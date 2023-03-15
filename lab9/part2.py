import Motor
import time
import cv2
import numpy as np

class Camera:

    def __init__(self, raspberrypi = True):
        
        self.rpi = raspberrypi
       
        if raspberrypi:
            from picamera2 import Picamera2 
            self.camera = Picamera2()
            self.camera.configure(self.camera.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
            self.camera.start()
        else:
            self.camera = cv2.VideoCapture(0)
    
    def close(self):
        if not self.rpi:
            self.camera.release()

    def get(self):
        if self.rpi:
            return self.camera.capture_array()
        else:
            _, frame = self.camera.read()
            return frame

    def get_circles(self):
        frame = self.get()

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_val = np.array([40, 30, 20])
        upper_val = np.array([80, 255, 255])
        mask = cv2.inRange(hsv, lower_val, upper_val)
        
        result = cv2.bitwise_and(frame, frame, mask = mask)

        #cv2.imshow('result', result)

        gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        # Display the resulting frame
        gray = cv2.medianBlur(gray, 5)
        
        
        rows = gray.shape[0]
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, rows / 8,
                                   param1=100, param2=30,
                                   minRadius=1, maxRadius=100)
        return circles

    def get_largest_circle(self):
        circles = self.get_circles()
        if circles is None or len(circles) == 0:
            return None
        max_size = 0
        max_idx = 0
       
        circles = circles[0]

        for i in range(len(circles)):
            print(circles[i])
            if circles[i][2] > max_size:
                max_size = circles[i][2]
                max_idx = i

        return circles[max_idx]



camera = Camera()

PWM = Motor.Motor()

def stop():
    PWM.setMotorModel(0, 0, 0, 0)

def move(l, r):
    PWM.setMotorModel(l, l, r, r)

def run():

    #image is 640 by 480
    # center is (320, 240)
    #while True:
    #    print(camera.get_circles())

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
            stop()

        time.sleep(0.1)

if __name__ == '__main__':

    try:
        run()
    except KeyboardInterrupt:
        stop()
        
    camera.close()
    cv2.destroyAllWindows()
