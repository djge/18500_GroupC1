import pyrealsense2 as rs
import cv2
import numpy as np
import serial

import os
import time
from PIL import Image
import matplotlib.pyplot as plt
import math
from getsuncalc import get_suncalc
from constant import address, camera_height, winHeight, orientation

import LAOE

def main():
    pipeline = rs.pipeline()
    config = rs.config()
    pipeline.start()
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.bgr8, 30)
    front_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    side_cascade = cv2.CascadeClassifier('haarcascade_profileface.xml')

    horiz_fov = 87 #degrees
    vert_fov = 58
    blinds_state = winHeight

    dataRate = 9600
        
    f = open('depth.txt', 'w')
    #arduino = serial.Serial("COM3", dataRate, timeout=2)
    #arduino.open()

    try:
        while True:
            #fetches latest unread frames (better for single camera vs. poll_for_frames)
            unaligned_frames = pipeline.wait_for_frames()

            #align color and depth frames
            align = rs.align(rs.stream.color)
            frames = align.process(unaligned_frames)

            color_frame = frames.get_color_frame()
            depth_frame = frames.get_depth_frame()
            if not (color_frame and depth_frame):
                continue
            color_img = np.asanyarray(color_frame.get_data())

            colorizer = rs.colorizer()
            depth_img = np.asanyarray(colorizer.colorize(depth_frame).get_data())

            #Haar cascades only work with grayscale
            gray = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)

            front = front_cascade.detectMultiScale(gray, 1.1, 4)
            #side = side_cascade.detectMultiScale(gray, 1.1, 4)

            face = front #if len(front) != 0 else side

            horiz_angle = math.radians(horiz_fov/color_img.shape[1])
            vert_angle = math.radians(vert_fov/color_img.shape[0])
            
            origin = (color_img.shape[1]/2, color_img.shape[0]/2)
            face_distances = [] #array of tuples (x,y)

            for (x, y, w, h) in face:
                x_mid, y_mid = [int(x + w/2), int(y + h)]
                if x_mid > 0 and x_mid < color_img.shape[1] and y_mid > 0 and y_mid < color_img.shape[0]: 
                    d = depth_frame.get_distance(x_mid, y_mid)
                    
                    pixels_diff_x, pixels_diff_y = x_mid - origin[0],  origin[1] - y_mid
                    angle_x, angle_y = pixels_diff_x*horiz_angle, pixels_diff_y*vert_angle

                    face_z = d*math.sin(angle_y) + camera_height
                    face_y = d*math.cos(angle_y)*math.cos(angle_x)
                    face_x = d*math.cos(angle_y)*math.sin(angle_x)

                    face_distances.append((face_x, face_y, face_z))

                cv2.rectangle(color_img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            
            #put images next to each other to display
            display_images = np.hstack((color_img, depth_img))
            #Show CV window
            cv2.namedWindow('RealSense', cv2.WINDOW_KEEPRATIO)
            cv2.resizeWindow('RealSense', 426, 240)
            cv2.imshow('RealSense', display_images)

            #TODO: Find out which box (if there are multiple because of false positives) to use
            if face_distances:
                azimuth, altitude = get_suncalc(address)

                #photoresistor = arduino.readline().decode().rstrip()  # read photoresistor input

                # distance (from bottom of window) blinds should be
                # current_blinds_state = LAOE.LAOE(altitude, azimuth, orientation, face_distances[0], blinds_state, photoresistor)
                current_blinds_state = LAOE.LAOE(altitude, azimuth, orientation, face_distances[0], blinds_state, 0)
                print("FACE DISTANCE", face_distances[0])
                print("LAOE", current_blinds_state)
                move = blinds_state - current_blinds_state
                # print("Sending to Arduino: ", move)
                # send number of rotations and direction
                #arduino.write(move, move < 0)
                blinds_state = current_blinds_state
            else:
                #arduino.write(0)
                blinds_state = 0

            cv2.waitKey(30)
            

    finally:
        pipeline.stop()
        
if __name__ == '__main__':
    main()