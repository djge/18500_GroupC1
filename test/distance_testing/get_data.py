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
    f_counter = open('./distance_test_data/data_counter.txt', 'rw')
    front_cascade = cv2.CascadeClassifier('../../haarcascade_frontalface_default.xml')

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

        gray = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)

        face = front_cascade.detectMultiScale(gray, 1.1, 4)
        if len(face) == 0:
            print("WARNING: No faces found")
            return
        if len(face) > 1:
            print("WARNING: More than one face found")
            return

        for (x, y, w, h) in face:
            x_mid, y_mid = [int(x + w/2), int(y + h)]
            if x_mid > 0 and x_mid < color_img.shape[1] and y_mid > 0 and y_mid < color_img.shape[0]:
                np.save('./distance_test_data/color' + f_counter +'.npy', color_img)
                f = open('./distance_test_data/depth' + f_counter + '.txt', 'w')
                f.write(str(depth_frame.get_distance(x_mid, y_mid)))
                f.close()
            else:
                print("WARNING: Chin pixel is out of image")
                return
    finally:
        pipeline.stop()

    f_counter.write(str(int(datapoint_num) + 1))
    f_counter.close()
        
if __name__ == '__main__':
    main()