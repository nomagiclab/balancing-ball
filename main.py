#!/usr/bin/env python3
import pybullet as p
import time
import argparse
from utils.environment import init_env_and_load_assets, update_wind_controllers, \
    BALL_DEFAULT_ORIENTATION, MAX_BALL_HEIGHT, BALL_DEFAULT_POSITION
from utils.button import Button


def get_mode():
    parser = argparse.ArgumentParser(description='Mode manager')

    parser.add_argument('--mode', dest='mode', type=str, help="Steering mode.")
    args = parser.parse_args()

    return args.mode == 'keyboard'


keyboard_mode = get_mode()

ballId, paddle, wind_controllers = init_env_and_load_assets(p)


if keyboard_mode:
    # add rotation speed controller
    rotation_speed_id = p.addUserDebugParameter("rotation_speed", 0, 45, 5)
    paddle.move_by_vector([0, 0, 0.5])

else:
    paddle.create_joint_controllers()

# Ball buttons
setBallInitHeight = p.addUserDebugParameter("Set initial ball height", 0, MAX_BALL_HEIGHT, BALL_DEFAULT_POSITION[2])
resetBallButton = Button(p.addUserDebugParameter("Reset ball position", 1, 0, 0))


while True:
    if keyboard_mode:
        paddle.steer_with_keyboard(p.readUserDebugParameter(rotation_speed_id))
    else:
        paddle.read_and_update_joint_position()

    # Reset ball position if button was clicked.
    if resetBallButton.wasClicked():
        height = p.readUserDebugParameter(setBallInitHeight)
        # Also sets velocity to 0.
        p.resetBasePositionAndOrientation(ballId, [BALL_DEFAULT_POSITION[0], BALL_DEFAULT_POSITION[1], height],
                                          BALL_DEFAULT_ORIENTATION)

    update_wind_controllers(p, *wind_controllers)

    p.stepSimulation()

    time.sleep(0.01)  # sometimes pybullet crashes, this line helps a lot
