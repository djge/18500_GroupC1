import pyrealsense2 as rs
import cv2
import numpy as np
import serial
import math
from getsuncalc import get_suncalc, test_suncalc
from constant import address, camera_height, winHeight, orientation, fullTurn, rotation

import LAOE

def main():
    pipeline = rs.pipeline()
    config = rs.config()
    pipeline.start()
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.bgr8, 30)
    front_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt_tree.xml')
    side_cascade = cv2.CascadeClassifier('haarcascade_profileface.xml')

    horiz_fov = 87 #degrees
    vert_fov = 58
    blinds_state = winHeight

    dataRate = 9600
    arduino = serial.Serial("/dev/ttyACM0", dataRate, timeout=2)
    sample_size = 5
    stopCommand = "stop"
    lightCommand = "light"
    currentDir = "forward"
    available = "Available" in arduino.readline().decode().strip()
    #print("1", available)

    try:
        sample = []
        while True:
            #if not available, read for availability
            if (not available):
                available = "Available" in arduino.readline().decode().strip()
                #print("2", available)

            #take samples
            if len(sample) < sample_size:
                #print("Taking Sample")
                unaligned_frames = pipeline.wait_for_frames()

                align = rs.align(rs.stream.color)
                frames = align.process(unaligned_frames)

                color_frame = frames.get_color_frame()
                depth_frame = frames.get_depth_frame()
                if not (color_frame and depth_frame):
                    continue
                color_img = np.asanyarray(color_frame.get_data())
                gray = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)

                front = front_cascade.detectMultiScale(gray, 1.1, 4)
                side = side_cascade.detectMultiScale(gray, 1.1, 4)

                face = front if len(front) != 0 else side

                horiz_angle = math.radians(horiz_fov/color_img.shape[1])
                vert_angle = math.radians(vert_fov/color_img.shape[0])
                
                origin = (color_img.shape[1]/2, color_img.shape[0]/2)
                face_distances = []

                isZero = False

                for (x, y, w, h) in face:
                    x_mid, y_mid = [int(x + w/2), int(y + h)]
                    if x_mid > 0 and x_mid < color_img.shape[1] and y_mid > 0 and y_mid < color_img.shape[0]: 
                        d = depth_frame.get_distance(x_mid, y_mid)
                        if d == 0:
                            isZero = True
                            break
                        pixels_diff_x, pixels_diff_y = x_mid - origin[0],  origin[1] - y_mid
                        angle_x, angle_y = pixels_diff_x*horiz_angle, pixels_diff_y*vert_angle
                        face_z = d*math.sin(angle_y) + camera_height
                        face_y = d*math.cos(angle_y)*math.cos(angle_x)
                        face_x = -d*math.cos(angle_y)*math.sin(angle_x)
                        face_distances.append((face_x, face_y, face_z))

                if face_distances and not isZero:
                    closest_face = min(face_distances, key = lambda t: math.sqrt(t[0]**2 + t[1]**2 + t[2]**2))
                    #PHOTORESISTOR 1
                    #azimuth, altitude = get_suncalc(address)
                    #fake azimuth/altitude
                    azimuth, altitude = test_suncalc(address)
                    
                    photoresistor = "1"
                    if (available):
                        arduino.write(lightCommand.encode())
                        photoresistor = arduino.readline().decode().rstrip()  # read photoresistor input
                        #print("3", photoresistor)
                        available = False

                        # distance (from bottom of window) blinds should be
                        # current_blinds_state = LAOE.LAOE(altitude, azimuth, orientation, face_distances[0], blinds_state, photoresistor)
                        LAOE_output = LAOE.LAOE(altitude, azimuth, orientation, closest_face, "1")
                        sample.append(LAOE_output)
                        move = "forwards, 0"
                else:
                    sample.append((False, 0))
                cv2.waitKey(30)
                print(sample)
            else:
                print("SAMPLE", sample)
                num_true = 0
                for i in range(sample_size):
                    if sample[i][0]: num_true += 1
                
                if num_true >= sample_size//2:
                    current_blinds_state = sample[sample_size-1][1]
                    for index in range(sample_size - 1, -1, -1):
                        if sample[index]:
                            current_blinds_state = sample[index][1]
                            
                    change = blinds_state - current_blinds_state
                    if change > 0:
                        #move = f"backward, {abs(change) * fullTurn // rotation}"
                        #currentDir = "backward"
                        move = f"forward, {abs(change) * fullTurn // rotation}"
                        currentDir = "forward"
                        # send number of rotations and direction
                        
                    elif change < 0:
                        #move = f"forward, {abs(change) * fullTurn // rotation}"
                        #currentDir = "forward"
                        move = f"backward, {abs(change) * fullTurn // rotation}"
                        currentDir = "backward"
                    
                    if (available):
                        print(move)
                        arduino.write(move.encode())
                        available = False
                        blinds_state = current_blinds_state
                #print("LAOE", current_blinds_state)
                #only need to stop if blinds are 
                elif not available and num_true == 0:             
                    print("STOP1")
                    arduino.write(stopCommand.encode())
                    remaining = arduino.readline().decode().rstrip()
                    if "Available" in remaining:
                        available = True
                        continue
                    #print("4", remaining)
                    #remaining is either numeric or has "invalid"
                    # while (not remaining.isnumeric() and "Invalid" not in remaining):
                    while (not remaining.isnumeric()):
                        #print("STOP2")
                        remaining = (arduino.readline().decode().rstrip())
                        if "Available" in remaining:
                            available = True
                            continue
                    if available:
                        continue
                    #if (remaining.isnumeric()):
                    remainingN = float(remaining) * rotation // fullTurn
                    
                    #if (currentDir == "forward"):
                    if (currentDir == "backward"):
                        blinds_state -= remainingN
                    else:
                        blinds_state += remainingN
                else:
                    change = winHeight - blinds_state
                    move = f"backward, {abs(change) * fullTurn // rotation}"
                    arduino.write(move.encode())
                    blinds_state = winHeight
                    available = False

                sample = []
    finally:
        pipeline.stop()
        
if __name__ == '__main__':
    main()