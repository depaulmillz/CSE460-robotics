import Motor
import time
import cv2
import numpy as np
from Camera import *

camera = Camera()

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

        circle = camera.get_largest_circle()

        if circle is None:
            sensed = False
        else:
            sensed = True
        
        if not sensed:
            move(-1500, 1500)
        else:

            # higher width is to the right
            # lower width is to the left
            
            # move left if width (circle[0] > 320) and right if (circle[0] < 320)

            K = 100

            angle = 320 - circle[0]
            
            # if angle < 0 then means move to the right (clockwise)
            move(-K * angle, K * angle)

            #stop()

        time.sleep(0.1)

if __name__ == '__main__':

    try:
        run()
    except KeyboardInterrupt:
        stop()
        
    camera.close()
    cv2.destroyAllWindows()

