import socket
import time
import sys
from NatNetClient import NatNetClient
from util import quaternion_to_euler_angle_vectorized1
import numpy as np

positions = {}
rotations = {}

# This is a callback function that gets connected to the NatNet client. It is called once per rigid body per frame
def receive_rigid_body_frame(robot_id, position, rotation_quaternion):
    # Position and rotation received
    positions[robot_id] = position
    # The rotation is in quaternion. We need to convert it to euler angles

    rotx, roty, rotz = quaternion_to_euler_angle_vectorized1(rotation_quaternion)

    rotations[robot_id] = rotz

class Position:

    def __init__(self, clientAddress, optitrackServerAddress, robot_id):
        self.robot_id = robot_id
        # This will create a new NatNet client
        self.streaming_client = NatNetClient()
        self.streaming_client.set_client_address(clientAddress)
        self.streaming_client.set_server_address(optitrackServerAddress)
        self.streaming_client.set_use_multicast(True)
        # Configure the streaming client to call our rigid body handler on the emulator to send data out.
        self.streaming_client.rigid_body_listener = receive_rigid_body_frame
        if not self.streaming_client.run():
            raise Exception("Not running")
       
    def get(self):
        while True:
            if self.robot_id in positions:
                #print('Last position', positions[robot_id], ' rotation', rotations[robot_id])
                return (positions[self.robot_id], rotations[self.robot_id])
                
class Robot:

    def __init__(self, IP_ADDRESS):
        # Connect to the robot
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((IP_ADDRESS, 5000))
            print('Connected to robot')
        except Exception:
            raise Exception("Could not connect to robot")

    def set_motor(self, a, b, c, d):
        command = 'CMD_MOTOR#%d#%d#%d#%d\n'%(int(a), int(b), int(c), int(d))
        self.s.send(command.encode('utf-8'))

    def stop_motor(self):
        command = 'CMD_MOTOR#00#00#00#00\n'
        self.s.send(command.encode('utf-8'))

    def shutdown(self):
        self.s.shutdown(2)
        self.s.close()

