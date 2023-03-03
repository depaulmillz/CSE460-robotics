import numpy as np
import apis
import time

if __name__ == "__main__":

    x_d = np.array([5.0, 3.5])
    #x_d = np.array([1.0, 0.0])

    IP_ADDRESS = '192.168.0.207'

    robot = apis.Robot(IP_ADDRESS)
   
    print("Starting")
    try:
        clientAddress = "192.168.0.25"
        optitrackServerAddress = "192.168.0.4"
        robot_id = 207
        
        # Start up the streaming client now that the callbacks are set up.
        # This will run perpetually, and operate on a separate thread.

        position = apis.Position(clientAddress, optitrackServerAddress, robot_id)

        K1 = 1000
        K2 = 7000 #500

        desiredAngle = None

        start = time.time()
        while True:

            xyz, rot = position.get()
            x, y, _ = xyz

            x_t = np.array([x, y])

            err = x_d - x_t

            dist = np.linalg.norm(err)

            #print("Dist", dist, x_t)

            desiredAngle = np.arctan2(err[1], err[0])

            #print("Distance", dist)

            angle = rot / 180 * np.pi

            angleDiff = np.arctan2(np.sin(desiredAngle - angle) , np.cos(desiredAngle - angle))

            print(angleDiff)

            if dist <= 0.2:
                robot.stop_motor()
                break

            v = K1 * dist

            omega = K2 * angleDiff;

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

