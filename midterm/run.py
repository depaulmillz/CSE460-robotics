import numpy as np
import apis
import time
import sys

if __name__ == "__main__":

    IP_ADDRESS = '192.168.0.207'

    robot = apis.Robot(IP_ADDRESS)
   
    print("Starting")
    try:
        # hostname = socket.gethostname()
        # ip_addr = socket.gethostbyname(hostname)
        clientAddress = "192.168.0.25"
        optitrackServerAddress = "192.168.0.4"
        robot_id = 207
        
        # Start up the streaming client now that the callbacks are set up.
        # This will run perpetually, and operate on a separate thread.

        position = apis.Position(clientAddress, optitrackServerAddress, robot_id)

        K1 = 1500#100
        K2 = 3000
        
        start = time.time()

        x_t, angle = position.get()

        path = apis.Path(start, 10, x_t, np.array([5.0, 2.5]))

        while True:
            x_t, angle = position.get()

            x_d = path.next(time.time())

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

