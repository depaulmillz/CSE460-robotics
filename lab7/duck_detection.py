from CameraAndDetector import *
import cv2

def distance(s):
    return 2421.692084 / s - 8.566887384

def theta(u):
    return -0.00172753493 * u + 0.5294127344

if __name__ == "__main__":

    camera = Camera(True)
    
    try:
        while True:
            _, gray = camera.get_blobs_and_gray()           
                       
            #cv2.imshow("detected circles", gray)
    
            cv2.imshow('frame',gray)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    except KeyboardInterrupt:
        pass
    
    camera.close()
    cv2.destroyAllWindows()
