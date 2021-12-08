#!/usr/bin/env python3
import argparse
import time

import pybullet as p

from controllers.pid_balancer import OUT_OF_RANGE
from utils.environment import init_env_and_load_assets, update_wind_controllers, init_standard_pid_tools


def get_mode():
    parser = argparse.ArgumentParser(description='Mode manager')

    parser.add_argument('--mode', dest='mode', type=str, help="Steering mode.")
    args = parser.parse_args()

    return args.mode


keyboard_mode = get_mode() == 'keyboard'

ball_controller, ball, paddle, wind_controllers = init_env_and_load_assets(p)

if keyboard_mode:
    # add rotation speed controller
    rotation_speed_id = p.addUserDebugParameter("rotation_speed", 0, 45, 5)
    paddle.move_by_vector([0, 0, 0.5])
else:
    paddle.create_joint_controllers()
    pid_sliders, pid_button, pid_balancer = init_standard_pid_tools(p, ball, paddle, 45, -45)

while True:
    if keyboard_mode:
        paddle.steer_with_keyboard(p.readUserDebugParameter(rotation_speed_id))
    else:
        paddle.read_and_update_joint_position()
        desired_angles = pid_balancer.calculate_next_angle()

        if desired_angles == OUT_OF_RANGE:
            paddle.reset_torque_pos()
        else:
            y_desired_angle, x_desired_angle = pid_balancer.calculate_next_angle()
            paddle.set_angle_on_axis('x', x_desired_angle)
            # The y rotation direction is inverted,
            # so we have to take the negative value.
            paddle.set_angle_on_axis('y', -y_desired_angle)

        if pid_button.was_clicked():
            pid_balancer.change_pid_coefficients(*[float(p.readUserDebugParameter(slider_id))
                                                   for _, slider_id in pid_sliders.items()])

    ball_controller.check_and_update_rotation()
    ball_controller.check_if_drop_with_rotation()
    if ball_controller.should_throw_ball():
        ball_controller.throw_ball(paddle.get_center_position())

    update_wind_controllers(p, *wind_controllers)

    p.stepSimulation()

    time.sleep(0.01)  # sometimes pybullet crashes, this line helps a lot
