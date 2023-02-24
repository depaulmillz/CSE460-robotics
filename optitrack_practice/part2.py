import numpy as np
import apis
import time

if __name__ == "__main__":

    x_d = np.array([2.0, 3.0])

    IP_ADDRESS = '192.168.0.207'

    robot = apis.Robot(IP_ADDRESS)
   
    print("Starting")
    try:
        # hostname = socket.gethostname()
        # ip_addr = socket.gethostbyname(hostname)
        clientAddress = "192.168.0.6"
        optitrackServerAddress = "192.168.0.4"
        robot_id = 207
        
        # Start up the streaming client now that the callbacks are set up.
        # This will run perpetually, and operate on a separate thread.

        position = apis.Position(clientAddress, optitrackServerAddress, robot_id)

        K1 = 500#100
        K2 = 2000 #500

        desiredAngle = None

        start = time.time()
        while True:
            xyz, rot = position.get()
            x, y, _ = xyz

            x_t = np.array([x, y])

            err = x_d - x_t

            dist = np.linalg.norm(err)

            #print("Dist", dist, x_t)

            if desiredAngle is None:
                desiredAngle = np.arctan(err[1] / err[0])

            print(desiredAngle - rot * np.pi / 180, dist, time.time() - start, sep=",")

            #print("Distance", dist)

            v = K1 * dist
            omega = K2 * (desiredAngle - rot * np.pi / 180);

           # print("Omega", omega, "v", v)

            u = np.array([v - omega, v + omega])
            u[u > 1500.] = 1500.
            u[u < -1500.] = -1500.
            #print("u", u)        
            
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

