#!/usr/bin/env python3
import pybullet as p
import time
import argparse
from utils.physics import get_force_vector
from utils.button import Button
from utils.environment import init_env_and_load_assets, update_wind_controllers


def get_mode():
    parser = argparse.ArgumentParser(description='Mode manager')

    parser.add_argument('--mode', dest='mode', type=str, help="Steering mode.")
    args = parser.parse_args()

    return args.mode == 'keyboard'


keyboard_mode = get_mode()

ball, paddle, wind_controllers = init_env_and_load_assets(p)


if keyboard_mode:
    # add rotation speed controller
    rotation_speed_id = p.addUserDebugParameter("rotation_speed", 0, 45, 5)
    paddle.move_by_vector([0, 0, 0.5])

else:
    paddle.create_joint_controllers()

throw_ball_button = Button(p.addUserDebugParameter("Throw ball towards paddle", 1, 0, 0))

while True:
    if keyboard_mode:
        paddle.steer_with_keyboard(p.readUserDebugParameter(rotation_speed_id))
    else:
        paddle.read_and_update_joint_position()

    ball.check_if_drop_with_rotation(p)
    ball.check_and_update_rotation(p)

    update_wind_controllers(p, *wind_controllers)

    # Check if the throw button was clicked, and throw the ball if so.
    if throw_ball_button.was_clicked():
        curr_ball = p.getBasePositionAndOrientation(ball.id)[0]
        curr_paddle = paddle.get_center_position()
        vec = get_force_vector(curr_ball, curr_paddle)
        p.applyExternalForce(ball.id, -1, vec, [0, 0, 0], p.WORLD_FRAME)

    p.stepSimulation()

    time.sleep(0.01)  # sometimes pybullet crashes, this line helps a lot
