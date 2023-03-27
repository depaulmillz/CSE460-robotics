import Motor
import time
import cv2
import numpy as np
from CameraAndDetector import *

camera = Camera(True)

PWM = Motor.Motor()

def stop():
    PWM.setMotorModel(0, 0, 0, 0)

def move(l, r):
    PWM.setMotorModel(l, l, r, r)

def run():

    #image is 640 by 480
    # center is (320, 240)

    sensed = False

    while True:

        circle, img = camera.get_largest_blob_and_img()

        if circle is None:
            sensed = False
        else:
            sensed = True
        
        if not sensed:
            move(-1000, 1000)
        else:

            # higher width is to the right
            # lower width is to the left
            
            # move left if width (circle[0] > 320) and right if (circle[0] < 320)

            K = 1

            angle = 320 - circle[0]
            
            # if angle < 0 then means move to the right (clockwise)
            move(-K * angle, K * angle)

            #stop()
        
        cv2.imshow('frame', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(0.1)

if __name__ == '__main__':

    try:
        run()
    except KeyboardInterrupt:
        stop()
        
    camera.close()
    cv2.destroyAllWindows()

