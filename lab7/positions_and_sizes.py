from CameraAndDetector import *
import cv2

if __name__ == "__main__":

    for i in range(1, 11):
        camera = Camera(read_img = True, img_name = "images/image" + str(i) + ".jpg")
        blob = camera.get_largest_blob()        
        print(blob[0], blob[1], blob[2], sep="\t")
        camera.close()
