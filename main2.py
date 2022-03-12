#!/usr/bin/env python3
import argparse
import time

import pybullet as p

from utils.environment import init_env_and_load_assets, update_wind_controllers
from utils.pid_performer import PidPerformer
from robot_interactions.robot_paddle import RobotPaddle
from paddle.mutual_robot_pybullet_paddle import BiPaddle


def get_mode():
    parser = argparse.ArgumentParser(description="Mode manager")

    parser.add_argument("--mode", dest="mode", type=str, help="Steering mode.")
    parser.add_argument("--pid", action="store_true")
    args = parser.parse_args()

    return args.mode, args.pid


mode, pid_flag = get_mode()
keyboard_mode = mode == "keyboard"

ball_controller, ball, paddle, wind_controllers = init_env_and_load_assets(p)

if keyboard_mode:
    # add rotation speed controller
    rotation_speed_id = p.addUserDebugParameter("rotation_speed", 0, 45, 5)
    paddle.move_by_vector([0, 0, 0.5])
else:
    paddle.create_joint_controllers()

# IP_ADDRESS = "10.20.4.170"
IP_ADDRESS = "192.168.0.89"

robot = RobotPaddle(IP_ADDRESS)
biPaddle = BiPaddle(paddle, robot)
input("Press Enter to start")

if pid_flag:
    pid_performer = PidPerformer(p, ball, biPaddle)

while True:
    if keyboard_mode:
        paddle.steer_with_keyboard(p.readUserDebugParameter(rotation_speed_id))
    else:
        paddle.read_and_update_joint_position()

    if pid_flag:
        pid_performer.perform_pid_step()

    ball_controller.check_and_update_rotation()
    ball_controller.check_if_drop_with_rotation()
    if ball_controller.should_throw_ball():
        ball_controller.throw_ball(paddle.get_center_position())

    update_wind_controllers(p, *wind_controllers)

    p.stepSimulation()

    time.sleep(0.01)  # sometimes pybullet crashes, this line helps a lot
