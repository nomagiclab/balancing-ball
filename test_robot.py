#!/usr/bin/env python3
import math
import time

import robot_interactions.robot_paddle as robot_paddle

IP_ADDRESS = "192.168.0.89"

paddle = robot_paddle.RobotPaddle(IP_ADDRESS)

paddle.update_tcp_info()
time.sleep(0.02)

print("tcp position = ", paddle.get_center_orientation())
time.sleep(1)


# ---------------------------------
paddle.rotate_around_axis("x", 45)
time.sleep(5)
paddle.update_tcp_info()
time.sleep(0.2)
print("tcp position = ", paddle.get_center_orientation())

# -----------------------------------------

paddle.rotate_around_axis("x", -90)
time.sleep(10)
paddle.update_tcp_info()
time.sleep(0.02)
print("tcp position = ", paddle.get_center_orientation())

paddle.stop()
