import cv2
import numpy as np
from enum import Enum

class Duck(Enum):
    SMALL_DUCK = ([0, 78, 185],[32, 255, 255])

class Camera:

    def __init__(self, raspberrypi = False, read_img = False, img_name = ""):
        
        self.rpi = raspberrypi
      
        self.read_img = read_img
        self.img_name = img_name

        if not read_img:

            if raspberrypi:
                from picamera2 import Picamera2 
                self.camera = Picamera2()
                self.camera.configure(self.camera.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
                self.camera.start()
            else:
                self.camera = cv2.VideoCapture(0)
    
    def close(self):
        if not self.rpi and not self.read_img:
            self.camera.release()

    def get(self):
        if self.read_img:
            img = cv2.imread(self.img_name)
            return cv2.resize(img, (640, 480))
        if self.rpi:
            return self.camera.capture_array()
        else:
            _, frame = self.camera.read()
            return frame

    def get_blobs_and_gray(self, color = Duck.SMALL_DUCK):
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

        #result = cv2.morphologyEx(result, cv2.MORPH_OPEN, kernel)
        #result = cv2.morphologyEx(result, cv2.MORPH_CLOSE, kernel)
        #
        #cv2.imshow('result', result)

        result = cv2.bitwise_not(result)
        
        gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

        # Display the resulting frame
        gray = cv2.medianBlur(gray, 11)

        #_, gray = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

        params = cv2.SimpleBlobDetector_Params()

        params.minThreshold = 100;
        params.maxThreshold = 255;
         
        # Filter by Area.
        params.filterByArea = True
        params.minArea = 1000
        params.maxArea = 2**64
         
        # Filter by Circularity
        params.filterByCircularity = False
        params.minCircularity = 0.1
         
        # Filter by Convexity
        params.filterByConvexity = False
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
    
    def get_blobs(self, color = Duck.SMALL_DUCK):
        blobs, _ = self.get_blobs_and_gray(color)
        return blobs
    
    def get_largest_blob(self, color = Duck.SMALL_DUCK):
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
 
    def get_largest_blob_and_img(self, color = Duck.SMALL_DUCK):
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
    
