#!/usr/bin/env python3
from  math import pi
import time

import robot_interactions.robot_paddle as robot_paddle

IP_ADDRESS = "192.168.0.89"

INITIAL_JOINT_POSITION = [-pi / 2, -pi / 2, -pi / 2, -pi, -pi / 2, 0]

paddle = robot_paddle.RobotPaddle(IP_ADDRESS, INITIAL_JOINT_POSITION)

paddle.update_tcp_info()
time.sleep(0.02)

print("tcp position = ", paddle.get_center_orientation())

ROTATE = 0
MOVE_JOINT = 1
MOVE_ONLY_ONE_WRIST = 2
RESET_POSITION = 3
while True:
    paddle.update_tcp_info()
    print("center position =", paddle.get_center_position())
    print("center orientation =", paddle.get_center_orientation())
    print("Joints position =", paddle.get_joints_position())
    order = int(input(f'What order you want to make {ROTATE} = rotate, '
                      f'{MOVE_JOINT} = move to joint position, '
                      f'{MOVE_ONLY_ONE_WRIST} = move_only_one_wrist, '
                      f'{RESET_POSITION} = reset position: '))
    if order == ROTATE:
        axis = input("What axis (x, y, z): ")
        angle = float(input("Angle after rotation (degrees): "))
        paddle.set_angle_on_axis_sync(axis, angle)
    elif order == MOVE_JOINT:
        print("Enter all 6 positions: ")
        position = [float(input()) for _ in range(6)]
        paddle.move_robot_to_position(position)
    elif order == MOVE_ONLY_ONE_WRIST:
        print("What index (starting from 0): ")
        new_wrist_position = float(input("Enter new position: "))
    elif order == RESET_POSITION:
        print("Resetting position...")
        paddle.move_robot_to_position(INITIAL_JOINT_POSITION)
    print("")


