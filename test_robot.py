#!/usr/bin/env python3

import time

import robot_interactions.robot_paddle as robot_paddle

paddle = robot_paddle.RobotPaddle()
time.sleep(0.02)
paddle.move_by_vector([0.4, 0.3, 0.5, 0, 0, 0])
time.sleep(3)
paddle.stop()
