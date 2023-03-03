import numpy as np
import apis
import time
import sys

sys.path.insert(0, "..")

import trajectory.piecewise as piecewise

def spline():
    _, x, y, _, _ = piecewise.spline_2d([5., -3.8, -3.8, 5., 5.], [3.5, 3.5, -2.5, -2.5, 3.5], [0.,-1, -1.0, 0.,1,0.], [0.,0.,-1,0.,1], [0., 1, 2, 3, 4], 100)
    return [np.array([i, j]) for i,j in zip(x,y)]

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
        K2 = 1500

        desiredAngle = None

        xyz, rot = position.get()


        x_t = np.array([xyz[0], xyz[0]])

        positions = spline()#[np.array([5.,2.]), np.array([6.,2.]), np.array([6.,3.]), np.array([5.,3.])]
       
        #print(positions)

        start = time.time()

        pos = 0

        x_d = np.copy(positions[pos])

        err = x_d - x_t
        desiredAngle = np.arctan2(err[1], err[0])

        print("robotx", "roboty", "desiredx", "desiredy", sep=",")

        while True:
            xyz, rot = position.get()
            x, y, _ = xyz

            x_t = np.array([x, y])

            err = x_d - x_t

            #print(err)

            dist = np.linalg.norm(err)

            angle = rot / 180 * np.pi
            desiredAngle = np.arctan2(err[1], err[0])

            while dist <= 0.4:
                pos += 1
                pos = pos % (len(positions) - 1)
                x_d = np.copy(positions[pos])
                err = x_d - x_t
                dist = np.linalg.norm(err)
                desiredAngle = np.arctan2(err[1], err[0])
                
            #print(x_d, x_t)

            #print(desiredAngle - rot, dist, time.time() - start, sep=",")

            #print("Distance", dist

            print(x_t[0], x_t[1], x_d[0], x_d[1], sep=",")

            v = K1 * dist
            angleDiff = np.arctan2(np.sin(desiredAngle - angle) , np.cos(desiredAngle - angle))
            omega = K2 * angleDiff

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

