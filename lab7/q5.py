from CameraAndDetector import *
import cv2
import apis
import time

def distance_duck(s):
    return 2421.692084 / s - 8.566887384

def theta_duck(u):
    return -0.00172753493 * u + 0.5294127344

if __name__ == "__main__":

    camera = Camera(raspberrypi = True)
        
    blobs = camera.get_blobs()           
            
    if blobs is not None:
        for blob in blobs[0, :]:
            print("theta", theta_duck(blob[0]))
            print("dist", distance_duck(blob[2]))
   
    camera.close()
    cv2.destroyAllWindows()
