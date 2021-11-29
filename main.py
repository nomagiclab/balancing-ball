#!/usr/bin/env python3
import pybullet as p
import time
import argparse
from utils import load_assets_only_paddle
from utils.button import Button
from utils.command_wrapper import CommandWrapper

DEFAULT_BALL_HEIGHT = 1
MAX_BALL_HEIGHT = 2
G = 9.81
DEFAULT_ORIENTATION = p.getQuaternionFromEuler([0, 0, 0])

parser = argparse.ArgumentParser(description='Mode manager')

parser.add_argument('--mode', dest='mode', type=str, help="Steering mode.")
args = parser.parse_args()

keyboard_mode = args.mode == 'keyboard'

# start the simulation with a GUI (p.DIRECT is without GUI)
p.connect(p.GUI)

ballId, paddle = load_assets_only_paddle(p)

if keyboard_mode:
    # add rotation speed controller
    rotation_speed_id = p.addUserDebugParameter("rotation_speed", 0, 45, 5)
    paddle.move_by_vector([0, 0, 0.5])

else:
    paddle.create_joint_controllers()

setBallInitHeight = p.addUserDebugParameter("Set initial ball height", 0, MAX_BALL_HEIGHT, DEFAULT_BALL_HEIGHT)
resetBallButton = Button(p.addUserDebugParameter("Reset ball position", 1, 0, 0))

p.stepSimulation()

reset_ball_val = 0
reset_paddle_val = 0

while True:
    if keyboard_mode:
        paddle.steer_with_keyboard(p.readUserDebugParameter(rotation_speed_id))
    else:
        paddle.read_and_update_joint_position()

    # Check if the reset button was clicked, and reset the ball eventually.
    if resetBallButton.wasClicked():
        height = p.readUserDebugParameter(setBallInitHeight)
        # Also sets velocity to 0.
        p.resetBasePositionAndOrientation(ballId, [0, 0, height], DEFAULT_ORIENTATION)

    p.stepSimulation()

    time.sleep(0.01)  # sometimes pybullet crashes, this line helps a lot
