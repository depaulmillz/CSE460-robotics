from CameraAndDetector import *
import cv2

if __name__ == "__main__":

    camera = Camera(read_img = True, img_name = "images/image1.jpg")
    
    try:
        _, gray = camera.get_blobs_and_gray()           
                       
        #cv2.imshow("detected circles", gray)
   
        img = camera.get()

        cv2.imshow('img', img)
        cv2.imshow('frame',gray)
        cv2.waitKey(0)
    
    except KeyboardInterrupt:
        pass
    
    camera.close()
    cv2.destroyAllWindows()
