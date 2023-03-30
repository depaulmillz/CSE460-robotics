from CameraAndDetector import *
import cv2

H_low = 0
H_high = 179
S_low= 0
S_high = 255
V_low= 0
V_high = 255

class color_class:
    def __init__(self, value):
        self.value = value

# https://blog.electroica.com/hsv-trackbar-opencv-python/
def callback(x):
    global H_low,H_high,S_low,S_high,V_low,V_high
    #assign trackbar position value to H,S,V High and low variable
    H_low = cv2.getTrackbarPos('low H','controls')
    H_high = cv2.getTrackbarPos('high H','controls')
    S_low = cv2.getTrackbarPos('low S','controls')
    S_high = cv2.getTrackbarPos('high S','controls')
    V_low = cv2.getTrackbarPos('low V','controls')
    V_high = cv2.getTrackbarPos('high V','controls')

if __name__ == "__main__":

    for i in range(1, 11):
        camera = Camera(read_img = True, img_name = "images/image" + str(i) + ".jpg")

        cv2.namedWindow('controls', cv2.WINDOW_NORMAL)

        cv2.createTrackbar('low H','controls',0,179,callback)
        cv2.createTrackbar('high H','controls',179,179,callback)

        cv2.createTrackbar('low S','controls',0,255,callback)
        cv2.createTrackbar('high S','controls',255,255,callback)

        cv2.createTrackbar('low V','controls',0,255,callback)
        cv2.createTrackbar('high V','controls',255,255,callback)

        try:
            while True:

                _, gray = camera.get_blobs_and_gray(color = color_class(([H_low, S_low, V_low],[H_high, S_high, V_high])))           
                               
                #cv2.imshow("detected circles", gray)
   
                img = camera.get()
                
                _, gray2 = camera.get_blobs_and_gray()           
                
                cv2.namedWindow('img', cv2.WINDOW_NORMAL)
                cv2.imshow('img', img)
                cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
                cv2.imshow('frame',gray)
                cv2.namedWindow('frame2', cv2.WINDOW_NORMAL)
                cv2.imshow('frame2',gray2)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        
        except KeyboardInterrupt:
            pass
        
        camera.close()
        cv2.destroyAllWindows()
