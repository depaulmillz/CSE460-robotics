from CameraAndDetector import *
import cv2
import apis
import time

def distance_duck(s):
    return 2421.692084 / s - 8.566887384

def theta_duck(u):
    return -0.00172753493 * u + 0.5294127344

class CirclePath:
    
    def __init__(self, position, factor, radius):
        self.start = time.time()
        self.init, _ = position.get()
        self.factor = factor
        self.radius = radius

    def get_next(self):
        t = time.time() - self.start
        if t / self.factor >= 2. * np.pi:
            return self.init
        return self.radius * np.array([np.sin(t/self.factor) + self.init[0], np.cos(t/self.factor) + self.init[1]])

if __name__ == "__main__":

    camera = Camera(True)
    robot = apis.LocalRobot()
    position = apis.Position("192.168.0.207", "192.168.0.4", 207)
    
    try:
        
        path = CirclePath(position, 3.0, 1.0)

        while True:
            blobs = camera.get_blobs()           

            x_t, angle = position.get()
            x_d = path.get_next()

            K1 = 1000
            K2 = 2000

            dist, desired_angle = apis.dist_and_angle(x_d, x_t)

            v = K1 * dist
            omega = K2 * apis.angle_diff(desired_angle, angle)

            u = np.array([v - omega, v + omega])

            robot.set_motor(u[0], u[0], u[1], u[1])

            time.sleep(0.1)
    
    except KeyboardInterrupt:
        pass
   
    robot.shutdown()
    camera.close()
    cv2.destroyAllWindows()
