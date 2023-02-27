import sim
import numpy as np
import sys

sys.path.insert(0, "..")

import trajectory.piecewise as piecewise

sim.simxFinish(-1)

clientID = sim.simxStart('127.0.0.1',19990,True,True,5000,5)

if clientID == -1:
    print("Connection refused")
    sys.exit(1)
else:
    print("Connected")

errorcode, motorLeft = sim.simxGetObjectHandle(clientID,'./leftMotor',sim.simx_opmode_oneshot_wait)

if errorcode != 0:
    print("Error unable to get left motor", errorcode)

errorcode, motorRight = sim.simxGetObjectHandle(clientID,'./rightMotor',sim.simx_opmode_oneshot_wait)

if errorcode != 0:
    print("Error, unable to get right motor", errorcode)


errorcode, robot = sim.simxGetObjectHandle(clientID, '/PioneerP3DX', sim.simx_opmode_oneshot_wait)

if errorcode != 0:
    print("Error unable to get robot handle", errorcode)

worldframe = -1

### Points
X_ = [0.0, 1.0, 1.0, 0.0, 0.0]
Y_ = [0.0, 0.0, 1.0, 1.0, 0.0]
Vx_ = [0.5, 0.0, 0.5, 0.0, 0.5]
Vy_ = [0.0, 0.5, 0.0, 0.5, 0.0]
T_ = [0.0, 1.0, 2.0, 3.0, 4.0]

_, traj_x, traj_y, _, _ = piecewise.spline_2d(X_, Y_, Vx_, Vy_, T_)

x_d_points = [np.array([x, y]) for x, y in zip(traj_x, traj_y) ]
x_d = x_d_points[0]
count = 0

K1 = 1.0
K2 = 1.0


try:
    while True:

        errorcode, xyz= sim.simxGetObjectPosition(clientID, robot, worldframe, sim.simx_opmode_oneshot_wait)

        if errorcode != 0:
            print("Error", errorcode)

        x,y,_ = xyz
        errorcode, angles = sim.simxGetObjectOrientation(clientID, robot, worldframe, sim.simx_opmode_oneshot_wait)

        if errorcode != 0:
            print("Error", errorcode)

        _,_,angle = angles

        #print(xyz, angles)

        x_t = np.array([x, y])
            
        err = x_d - x_t
        dist = np.linalg.norm(err)

        if dist < 0.1:
            count += 1
            x_d = x_d_points[count % len(x_d_points)]
            err = x_d - x_t
            dist = np.linalg.norm(err)
        
        desiredAngle = np.arctan2(err[1], err[0])
        
        angleDiff = np.arctan2(np.sin(desiredAngle - angle) , np.cos(desiredAngle - angle))

        #((desiredAngle - angle + np.pi) % (2 * np.pi)) - np.pi
        
        print("Angles: " + str(angle) + " " + str(desiredAngle) + " diff " + str(angleDiff))
        
        v = K1 * dist
        w = K2 * angleDiff

        sim.simxSetJointTargetVelocity(clientID, motorLeft, v - w, sim.simx_opmode_oneshot_wait)

        sim.simxSetJointTargetVelocity(clientID, motorRight, v + w, sim.simx_opmode_oneshot_wait)
except KeyboardInterrupt:
    sim.simxStopSimulation(clientID, sim.simx_opmode_oneshot_wait)
    print("Done")

sim.simxFinish(clientID)
