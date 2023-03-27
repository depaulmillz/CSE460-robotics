from CameraAndDetector import *
import cv2

if __name__ == "__main__":

    camera = Camera(False)
    
    try:
        while True:
            circles, gray = camera.get_circles_and_gray(Color.YELLOW)           
            
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
