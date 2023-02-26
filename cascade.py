import pyrealsense2 as rs
import cv2
import numpy as np

def main():
    pipeline = rs.pipeline()
    config = rs.config()
    pipeline.start()
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    front_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    side_cascade = cv2.CascadeClassifier('haarcascade_profileface.xml')
    try:
        while True:
            #fetches latest unread frames (better for single camera vs. poll_for_frames)
            frames = pipeline.wait_for_frames()
            #image frame
            color_frame = frames.get_color_frame()
            if not color_frame:
                continue
            color_img = np.asanyarray(color_frame.get_data())

            #Haar cascades only work with grayscale
            gray = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)

            front = front_cascade.detectMultiScale(gray, 1.1, 4)
            side = side_cascade.detectMultiScale(gray, 1.1, 4)
            
            face = front if len(front) != 0 else side
            for (x, y, w, h) in face:
                cv2.rectangle(color_img, (x, y), (x+w, y+h), (255, 0, 0), 2)

            #Show CV window
            cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('RealSense', color_img)
            cv2.waitKey(30)

    finally:
        pipeline.stop()
        
if __name__ == '__main__':
    main()