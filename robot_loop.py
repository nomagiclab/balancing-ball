#!/usr/bin/env python3
from math import pi
import time

import robot_interactions.robot_paddle as robot_paddle

IP_ADDRESS = "192.168.3.17"

INITIAL_JOINT_POSITION = [-pi / 2, -pi / 2, -pi / 2, -pi, -pi / 2, 0]

paddle = robot_paddle.RobotPaddle(IP_ADDRESS)

paddle.update_tcp_info()
time.sleep(0.02)

print("tcp position = ", paddle.get_center_orientation())

ROTATE = 0
ROTATE_RP = 1
MOVE_JOINT = 2
MOVE_ONLY_ONE_WRIST = 3
RESET_POSITION = 4

while True:
    paddle.update_tcp_info()
    print("center position =", paddle.get_center_position())
    print("center orientation =", paddle.get_center_orientation())
    print("Joints position =", paddle.get_joints_position())
    order = int(
        input(
            f"What order you want to make {ROTATE} = rotate, "
            f"{ROTATE_RP} = rotate_rp, "
            f"{MOVE_JOINT} = move to joint position, "
            f"{MOVE_ONLY_ONE_WRIST} = move_only_one_wrist, "
            f"{RESET_POSITION} = reset position: "
        )
    )
    if order == ROTATE:
        axis = input("What axis (x, y, z): ")
        angle = float(input("Angle after rotation (degrees): "))
        paddle.set_angle_on_axis_sync(axis, angle)
    if order == ROTATE_RP:
        r = float(input("Roll: "))
        p = float(input("Pitch: "))
        paddle.set_angles_rp(r, p)
    elif order == MOVE_JOINT:
        print("Enter all 6 positions: ")
        position = [float(input()) for _ in range(6)]
        paddle.move_robot_to_position(position)
    elif order == MOVE_ONLY_ONE_WRIST:
        print("What index (starting from 0): ")
        index = int(input())
        new_wrist_position = float(input("Enter new position: "))
        paddle.rotate_wrist(index, new_wrist_position)
    elif order == RESET_POSITION:
        print("Resetting position...")
        paddle.move_robot_to_position(INITIAL_JOINT_POSITION)
    print("")
