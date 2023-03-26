from Camera import *
import cv2

if __name__ == "__main__":

    camera = Camera()
    
    try:
        while True:
            circle = camera.get_largest_circle(Color.YELLOW)           
            print(circle)
               
    except KeyboardInterrupt:
        pass
    
    camera.close()
    cv2.destroyAllWindows()
