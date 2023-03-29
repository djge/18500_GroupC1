import numpy as np
import cv2
import math
from constant import address, camera_height, winHeight, orientation

def display(example_num):
    [color_img, x, y, w, h] = predict(example_num, display=True)
    cv2.rectangle(color_img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    while(True):
        cv2.namedWindow('RealSense', cv2.WINDOW_KEEPRATIO)
        cv2.resizeWindow('RealSense', 426, 240)
        cv2.imshow('RealSense', color_img)
        cv2.waitKey(30)

def calculate_error(predicted, real):
    error = [abs((predicted[i] - real[i])/real[i]) for i in range(3)]
    return error

def predict(example_num, display = False):
    front_cascade = cv2.CascadeClassifier('../../haarcascade_frontalface_default.xml')
    color_img = np.load('distance_test_data/color'+str(example_num)+'.npy') # load

    f = open("distance_test_data/depth"+str(example_num)+'.txt', "r")
    d = float(f.read())
    f.close()
    horiz_fov = 87 #degrees
    vert_fov = 58

    gray = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)

    front = front_cascade.detectMultiScale(gray, 1.1, 4)
    origin = (color_img.shape[1]/2, color_img.shape[0]/2)
    horiz_angle = math.radians(horiz_fov/color_img.shape[1])
    vert_angle = math.radians(vert_fov/color_img.shape[0])
    calculated_distance = []
    
    for (x, y, w, h) in front:
        if(display):
            return color_img, x, y, w, h
        x_mid, y_mid = [int(x + w/2), int(y + h)]
        pixels_diff_x, pixels_diff_y = x_mid - origin[0],  origin[1] - y_mid
        angle_x, angle_y = pixels_diff_x*horiz_angle, pixels_diff_y*vert_angle
        face_z = d*math.sin(angle_y) + camera_height
        face_y = d*math.cos(angle_y)*math.cos(angle_x)
        face_x = d*math.cos(angle_y)*math.sin(angle_x)
        
        calculated_distance.extend([face_x, face_y, face_z])
    
    return calculated_distance

def main():
    f_counter = open("./distance_test_data/data_counter.txt", 'r')
    example_num = f_counter.read()
    f_counter.close()
    f_data = open("./distance_test_data/measured_data.txt", 'r')

    avg_error = [0,0,0]
    
    for example in range(1, int(example_num)):
        calculated = predict(example)
        measured_data = f_data.readline().split(", ")
        measured_data = [float(element[2:]) for element in measured_data]
        avg_error = [(avg_error[i] + calculate_error(calculated, measured_data)[i]) for i in range(3)]
    f_data.close()

    avg_error = [element/(int(example_num) - 1) for element in avg_error]

    print("Average error:", avg_error)
    #can display a particular example
    #display(1)

if __name__ == '__main__':
    main()
