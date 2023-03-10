import cv2
import numpy as np

class Camera:

    def __init__(self, raspberrypi = False):
        
        self.rpi = raspberrypi
       
        if raspberrypi:
            from picamera2 import Picamera2 
            self.camera = Picamera2()
            self.camera.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
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


camera = Camera()

try:
    while True:
        frame = camera.get()

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # 95 to 125 for HUE
        # saturation in 50 to 255

        lower_blue = np.array([90, 25, 20])
        upper_blue = np.array([125, 255, 255])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        
        result = cv2.bitwise_and(frame, frame, mask = mask)

        cv2.imshow('result', result)

        gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        # Display the resulting frame
        gray = cv2.medianBlur(gray, 5)
        
        
        rows = gray.shape[0]
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, rows / 8,
                                   param1=100, param2=30,
                                   minRadius=1, maxRadius=100)
        
        
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                center = (i[0], i[1])
                # circle center
                cv2.circle(gray, center, 1, (0, 100, 100), 3)
                # circle outline
                radius = i[2]
                cv2.circle(gray, center, radius, (255, 0, 255), 3)
        
        
        #cv2.imshow("detected circles", gray)

        cv2.imshow('frame',gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    pass

camera.close()
cv2.destroyAllWindows()
