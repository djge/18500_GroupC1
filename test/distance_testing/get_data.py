import pyrealsense2 as rs
import cv2
import numpy as np
import math
from constant import camera_height

def main():
    pipeline = rs.pipeline()
    config = rs.config()
    pipeline.start()
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.bgr8, 30)
    front_cascade = cv2.CascadeClassifier('../../haarcascade_frontalface_default.xml')

    horiz_fov = 87 #degrees
    vert_fov = 58
    f_counter = open('./distance_test_data/data_counter.txt', 'rw')

    datapoint_num = f.read()
    try:
        unaligned_frames = pipeline.wait_for_frames()

        align = rs.align(rs.stream.color)
        frames = align.process(unaligned_frames)

        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()
        if not (color_frame and depth_frame):
            print("FRAME NOT FOUND")
            return
        color_img = np.asanyarray(color_frame.get_data())
        colorizer = rs.colorizer()
        depth_img = np.asanyarray(colorizer.colorize(depth_frame).get_data())

        gray = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)

        face = front_cascade.detectMultiScale(gray, 1.1, 4)
        if len(face) == 0:
            print("NO FACES FOUND")
            return

        horiz_angle = math.radians(horiz_fov/color_img.shape[1])
        vert_angle = math.radians(vert_fov/color_img.shape[0])
        
        origin = (color_img.shape[1]/2, color_img.shape[0]/2)
        face_distances = [] #array of tuples (x,y)

        for (x, y, w, h) in face:
            x_mid, y_mid = [int(x + w/2), int(y + h)]
            #save data of first face found
            np.save('./distance_test_data/color' + f_counter +'.npy', color_img)
            f = open('./distance_test_data/depth' + f_counter + '.txt', 'w')
            f.write(str(depth_frame.get_distance(x_mid, y_mid)))
            f.close()
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
    finally:
        pipeline.stop()

    f_counter.write(str(int(datapoint_num) + 1))
    f_counter.close()
        
if __name__ == '__main__':
    main()