import numpy as np
import apis
import time

#def circle(steps, init):
#    return [np.array([np.cos(s) + init[0], np.sin(s) + init[1]]) for s in steps]

def circle(t, init):
    return np.array([np.cos(t / 5.) + init[0], np.sin(t / 5.) + init[1]])

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

        K1 = 1000#100
        K2 = 1500

        desiredAngle = None

        xyz_, rot = position.get()


        #x_t = np.array([xyz[0], xyz[0]])

        #positions = circle(np.linspace(0, 2 * np.pi, 4), np.array([xyz[0], xyz[1]]))
        
        start = time.time()

        #pos = 0

        #x_d = np.copy(positions[pos])

        #err = x_d - x_t
        #desiredAngle = np.arctan2(err[1], err[0])
        #print(desiredAngle)
        
        print("robotx", "roboty", "desiredx", "desiredy", sep=",")

        while True:
            xyz, rot = position.get()
            x, y, _ = xyz

            x_d = circle(time.time() - start, np.array([xyz_[0], xyz_[1]]))

            x_t = np.array([x, y])

            err = x_d - x_t

            #print(err)

            dist = np.linalg.norm(err)

            angle = rot / 180 * np.pi
            desiredAngle = np.arctan2(err[1], err[0])


            #if dist <= 0.3:
                #print("Next")
            #    pos += 1
            #    pos = pos % len(positions)
            #    x_d = np.copy(positions[pos])
            #    err = x_d - x_t
            #    dist = np.linalg.norm(err)
            #    desiredAngle = np.arctan2(err[1], err[0])

            
            print(x_t[0], x_t[1], x_d[0], x_d[1], sep=",")
        
                
            #print(x_d, x_t)

            #print("Dist", dist, x_t)


            #print(desiredAngle - rot, dist, time.time() - start, sep=",")

            #print("Distance", dist)

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

