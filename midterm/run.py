import numpy as np
import apis
import time
import sys

factor = 3.0

def rot_mat(theta):
    return np.array([[np.cos(theta) , -np.sin(theta)], 
                     [np.sin(theta), np.cos(theta)]])

def elipse(a, b, t, init):
    return np.array([init[0] - a + a * np.cos(t / factor), init[1] + b * np.sin(t / factor)])

def rotated_elipse(a, b, t, init, theta):
    init_rot = np.matmul(rot_mat(-theta), init)
    return np.matmul(rot_mat(theta), elipse(a, b, t, init_rot))

if __name__ == "__main__":

    IP_ADDRESS = '192.168.0.207'

    robot = apis.Robot(IP_ADDRESS)
  
    duck = np.array([-2.220845937728882, -0.5739241242408752])
    box_width = .65

    print("Starting")
    try:
        # hostname = socket.gethostname()
        # ip_addr = socket.gethostbyname(hostname)
        clientAddress = "192.168.0.3"
        optitrackServerAddress = "192.168.0.4"
        robot_id = 207
        
        # Start up the streaming client now that the callbacks are set up.
        # This will run perpetually, and operate on a separate thread.

        position = apis.Position(clientAddress, optitrackServerAddress, robot_id)

        K1 = 2000#100
        K2 = 2500
        
        start = time.time()

        init, angle = position.get()

        dist, angleToDuck = apis.dist_and_angle(init, duck)
        
        a = dist / 2.0
        theta = angleToDuck
        
        print(rot_mat(theta))

        print(a, theta, angleToDuck)

        b = box_width
        
        while True:

            x_t, angle = position.get()

            curr = time.time() - start

            if curr < 2 * np.pi * factor - 0.1:
                x_d = rotated_elipse(a, b, curr, init, theta)

                if curr <= np.pi * factor - 0.1 and curr >= np.pi * factor + 0.1:
                    K1 = 2000
                    K2 = 2500
                else:
                    K2 = 2000
                    K1 = 4000

            else:
                K1 = 1000
                K2 = 2000
                x_d = init
            
            dist, desiredAngle = apis.dist_and_angle(x_d, x_t)

            v = K1 * dist
            angleDiff = apis.angle_diff(desiredAngle, angle)
            omega = K2 * angleDiff

            u = np.array([v - omega, v + omega])
            u[u > 1500.] = 1500.
            u[u < -1500.] = -1500.
            
            robot.set_motor(u[0], u[0], u[1], u[1])
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Shutting down")
        robot.stop_motor()
        time.sleep(1)
        robot.stop_motor()
        pass
    
    robot.stop_motor()
    robot.shutdown()
    print("Done")

