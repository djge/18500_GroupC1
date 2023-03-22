import pyrealsense2 as rs
import cv2
import numpy as np

import os
import time
from PIL import Image
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import matplotlib.pyplot as plt
import math
os.environ["TFHUB_DOWNLOAD_PROGRESS"] = "True"

#Minorly edited helper functions preprocess_image and save_image from https://www.tensorflow.org/hub/tutorials/image_enhancing
def preprocess_image(numpy_image):
  """ Loads image from path and preprocesses to make it model ready
      Args:
        image_path: Path to the image file
  """
  hr_image = tf.convert_to_tensor(numpy_image)
  # If PNG, remove the alpha channel. The model only supports
  # images with 3 color channels.
  if hr_image.shape[-1] == 4:
    hr_image = hr_image[...,:-1]
  hr_size = (tf.convert_to_tensor(hr_image.shape[:-1]) // 4) * 4
  hr_image = tf.image.crop_to_bounding_box(hr_image, 0, 0, hr_size[0], hr_size[1])
  hr_image = tf.cast(hr_image, tf.float32)
  return tf.expand_dims(hr_image, 0)

def save_image(image, filename):
  """
    Saves unscaled Tensor Images.
    Args:
      image: 3D image tensor. [height, width, channels]
      filename: Name of the file to save.
  """
  if not isinstance(image, Image.Image):
    image = tf.clip_by_value(image, 0, 255)
    image = Image.fromarray(tf.cast(image, tf.uint8).numpy())
  image.save("%s.jpg" % filename)
  print("Saved as %s.jpg" % filename)

def main():
    pipeline = rs.pipeline()
    config = rs.config()
    pipeline.start()
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.bgr8, 30)
    front_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    side_cascade = cv2.CascadeClassifier('haarcascade_profileface.xml')

    diagonal_FOV = 89 #degrees

    try:
        while True:
            #fetches latest unread frames (better for single camera vs. poll_for_frames)
            unaligned_frames = pipeline.wait_for_frames()

            #align color and depth frames
            align = rs.align(rs.stream.color)
            frames = align.process(unaligned_frames)

            #image frame
            color_frame = frames.get_color_frame()
            depth_frame = frames.get_depth_frame()
            if not (color_frame and depth_frame):
                continue
            color_img = np.asanyarray(color_frame.get_data())

            #get a colored depth image from frame
            colorizer = rs.colorizer()
            depth_img = np.asanyarray(colorizer.colorize(depth_frame).get_data())

            #Haar cascades only work with grayscale
            gray = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)

            front = front_cascade.detectMultiScale(gray, 1.1, 4)
            #side = side_cascade.detectMultiScale(gray, 1.1, 4)
            
            face = front #if len(front) != 0 else side
            
            #if no face detected, use super resolution
            '''
            if not face:
                color_img = preprocess_image(color_img).numpy()
                gray = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)
                face = front_cascade.detectMultiScale(gray, 1.1, 4)'''
            pixel_angle = diagonal_FOV / math.sqrt(color_img.shape[0]**2 + color_img.shape[1]**2)
            center_img = (color_img.shape[1]/2, color_img.shape[0]/2)
            face_distances = [] #array of tuples (x,y)

            for (x, y, w, h) in face:
                x_mid, y_mid = [int(x + w/2), int(y + h)]
                d = depth_frame.get_distance(x_mid, y_mid)
                #TODO: check if chin is even in camera to prevent crashes
                pixels_diff_x, pixels_diff_y = x_mid - center_img[0], y_mid - center_img[1]
                angle_diff_x, angle_diff_y = pixels_diff_x*pixel_angle, pixels_diff_y*pixel_angle
                distance_x, distance_y = d*math.sin(math.radians(angle_diff_x)), d*math.cos(math.radians(angle_diff_y))

                face_distances.append((distance_x, distance_y))

                cv2.rectangle(color_img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            
            #put images next to each other to display
            display_images = np.hstack((color_img, depth_img))
            #Show CV window
            cv2.namedWindow('RealSense', cv2.WINDOW_KEEPRATIO)
            #cv2.resizeWindow('RealSense', 426, 240)
            cv2.imshow('RealSense', display_images)
            cv2.waitKey(30)
            #TODO: pass (x,y) to LAOE algorithm
    finally:
        pipeline.stop()
        
if __name__ == '__main__':
    main()