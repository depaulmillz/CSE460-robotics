import cv2
import numpy as np
from enum import Enum

class Color(Enum):
    GREEN = ([25, 30, 20],[80, 255, 255])
    YELLOW = ([25, 55, 20],[35, 255, 255])

class Camera:

    def __init__(self, raspberrypi = False):
        
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

    def get_circles_and_gray(self, color = Color.GREEN):
        frame = self.get()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # 95 to 125 for HUE
        # saturation in 25 to 255

        # orange 15 to 25
        # saturation 25 to 255

        lower_val = np.array(color.value[0])
        upper_val = np.array(color.value[1])
        mask = cv2.inRange(hsv, lower_val, upper_val)
        #
        result = cv2.bitwise_and(frame, frame, mask = mask)


        
        #kernel = np.ones((5,5),np.uint8)

        #result = cv2.morphologyEx(result, cv2.MORPH_OPEN, kernel)
        #result = cv2.morphologyEx(result, cv2.MORPH_CLOSE, kernel)
        #
        #cv2.imshow('result', result)
        
        gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        # Display the resulting frame
        gray = cv2.medianBlur(gray, 5)

        
        
        rows = gray.shape[0]
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, rows / 8,
                                   param1=100, param2=30,
                                   minRadius=1, maxRadius=400)
        return circles, gray

    def get_blobs_and_gray(self, color = Color.YELLOW):
        frame = self.get()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # 95 to 125 for HUE
        # saturation in 25 to 255

        # orange 15 to 25
        # saturation 25 to 255

        lower_val = np.array(color.value[0])
        upper_val = np.array(color.value[1])
        mask = cv2.inRange(hsv, lower_val, upper_val)
        #
        result = cv2.bitwise_and(frame, frame, mask = mask)

        
        kernel = np.ones((11,11),np.uint8)

        result = cv2.morphologyEx(result, cv2.MORPH_OPEN, kernel)
        result = cv2.morphologyEx(result, cv2.MORPH_CLOSE, kernel)
        #
        #cv2.imshow('result', result)

        result = cv2.bitwise_not(result)
        
        gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

        # Display the resulting frame
        gray = cv2.medianBlur(gray, 11)

        _, gray = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

        params = cv2.SimpleBlobDetector_Params()

        params.minThreshold = 0;
        params.maxThreshold = 256;
         
        # Filter by Area.
        params.filterByArea = False
        params.minArea = 100
         
        # Filter by Circularity
        params.filterByCircularity = False
        params.minCircularity = 0.1
         
        # Filter by Convexity
        params.filterByConvexity = True
        params.minConvexity = 0.87
         
        # Filter by Inertia
        params.filterByInertia = False
        params.minInertiaRatio = 0.01

        detector = None

        ver = (cv2.__version__).split('.')
        if int(ver[0]) < 3 :
          detector = cv2.SimpleBlobDetector(params)
        else : 
          detector = cv2.SimpleBlobDetector_create(params)
      
        keypoints = detector.detect(gray)

        im_with_keypoints = cv2.drawKeypoints(gray, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)


        blobs = []

        for k in keypoints:
            blobs.append([k.pt[0], k.pt[1], k.size])

        if len(blobs) == 0:
            return None, im_with_keypoints

        return np.array([blobs]), im_with_keypoints

    def get_circles(self, color = Color.GREEN):
        circles, _ = self.get_circles_and_gray(color)
        return circles

    
    def get_blobs(self, color = Color.YELLOW):
        blobs, _ = self.get_blobs_and_grey(color)
        return blobs

    def get_largest_circle(self, color = Color.GREEN):
        circles = self.get_circles(color)
        
        if circles is not None:
            circles = np.uint16(np.around(circles))
            
            max_radius = -1
            max_circle = None

            for i in circles[0, :]:
                radius = i[2]
                if radius > max_radius:
                    max_radius = radius
                    max_circle = i
            return max_circle
        else:
            return None
    
    def get_largest_blob(self, color = Color.YELLOW):
        blobs = self.get_blobs(color)
        
        if blobs is not None:
            blobs = np.uint16(np.around(blobs))
            
            max_radius = -1
            max_circle = None

            for i in blobs[0, :]:
                radius = i[2]
                if radius > max_radius:
                    max_radius = radius
                    max_circle = i
            return max_circle
        else:
            return None
 
    def get_largest_blob_and_img(self, color = Color.YELLOW):
        blobs, gray = self.get_blobs_and_gray(color)
        
        if blobs is not None:
            blobs = np.uint16(np.around(blobs))
            
            max_radius = -1
            max_circle = None

            for i in blobs[0, :]:
                radius = i[2]
                if radius > max_radius:
                    max_radius = radius
                    max_circle = i
            return (max_circle, gray)
        else:
            return (None, gray)
 
    def get_largest_circle_and_img(self, color = Color.GREEN):
        circles, gray = self.get_circles_and_gray(color)
        
        if circles is not None:
            circles = np.uint16(np.around(circles))
            
            max_radius = -1
            max_circle = None

            for i in circles[0, :]:
                radius = i[2]
                if radius > max_radius:
                    max_radius = radius
                    max_circle = i

            if max_circle is not None:
                center = (max_circle[0], max_circle[1])
                # circle center
                cv2.circle(gray, center, 1, (0, 100, 100), 3)
                # circle outline
                radius = max_circle[2]
                cv2.circle(gray, center, radius, (255, 0, 255), 3)

            return (max_circle, gray)
        else:
            return (None, gray)

