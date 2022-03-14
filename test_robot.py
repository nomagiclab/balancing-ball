#!/usr/bin/env python3
from math import  pi
import time

import robot_interactions.robot_paddle as robot_paddle

IP_ADDRESS = "192.168.0.89"
#
# INITIAL_JOINT_POSITION = [
#     -1.6006999999999998,
#     -1.7271,
#     -2.2029999999999994,
#     -0.8079999999999998,
#     1.5951,
#     -0.030999999999999694,
# ]

INITIAL_JOINT_POSITION = [-pi / 2, -pi / 2, -pi / 2, -pi, -pi / 2, 0]

paddle = robot_paddle.RobotPaddle(IP_ADDRESS, INITIAL_JOINT_POSITION)
paddle.update_tcp_info()
print("tcp orientation = ", paddle.get_center_orientation())

axis = "x"

# ---------------------------------
paddle.set_angle_on_axis_sync(axis, -30)
paddle.update_tcp_info()
time.sleep(1)
print("tcp orientation = ", paddle.get_center_orientation())
time.sleep(3)
# -----------------------------------------

# paddle.rotate_around_axis_sync(axis, -15)
# paddle.update_tcp_info()
# time.sleep(1)
# print("tcp position = ", paddle.get_center_orientation())
# time.sleep(1)
# paddle.reset_torque_pos()
# paddle.stop()
