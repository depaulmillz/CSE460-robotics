import numpy as np
import apis

if __name__ == "__main__":

    IP_ADDRESS = '192.168.0.207'

    robot = apis.Robot(IP_ADDRESS)
    
    try:
        # hostname = socket.gethostname()
        # ip_addr = socket.gethostbyname(hostname)
        clientAddress = "192.168.0.9"
        optitrackServerAddress = "192.168.0.4"
        robot_id = 207
        
        # Start up the streaming client now that the callbacks are set up.
        # This will run perpetually, and operate on a separate thread.

        position = apis.Position(clientAddress, optitrackServerAddress, robot_id)

        # trajectory is [cos(at) sin(at)] + x_0
        # this means u(t) = [-asin(ax) acos(ax)]

        print("x", "y", "pred x", "pred y")
        start = None
        x_0 = None

        a = 1.0
        K = 500.0

        while True:
            xyz, _ = position.get()
            x, y, _ = xyz
           
            now = time.time()
            if start == None:
                x_0 = np.array([x, y])
                start = now

            t = now - start

            pd_prime = np.array([-a * np.sin(a * t), a * np.cos(a * t)])
            pd = np.array([np.cos(a * t), np.sin(a * t)]) + x_0
            pt = np.array([x, y])

            u = K * (pd - pt) + pd_prime

            u[u > 1500] = 1500
            u[u < -1500] = -1500

            robot.set_motor(u[0], u[0], u[1], u[1])
            
            print(pt[0], pt[1], pd[0], pd[1]) 
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Shutting down")
        robot.stop_motor()
        pass
    
    robot.shutdown()
    print("Done")

