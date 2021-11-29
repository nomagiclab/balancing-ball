#!/usr/bin/env python3
import pybullet as p
import time
import argparse
from utils import load_assets_only_paddle
import utils

parser = argparse.ArgumentParser(description='Mode manager')

parser.add_argument('--mode', dest='mode', type=str, help="Steering mode.")
args = parser.parse_args()

keyboard_mode = args.mode == 'keyboard'

# start the simulation with a GUI (p.DIRECT is without GUI)
p.connect(p.GUI)

ball, paddle = load_assets_only_paddle(p)

if keyboard_mode:
    # add rotation speed controller
    rotation_speed_id = p.addUserDebugParameter("rotation_speed", 0, 45, 5)
    paddle.move_by_vector([0, 0, 0.5])

else:
    paddle.create_joint_controllers()

reset_ball_button = p.addUserDebugParameter("Reset ball position", 1, 0, 0)
force_ball_button = p.addUserDebugParameter("Apply force to the ball", 1, 0, 0)

p.stepSimulation()

reset_ball_val = 0
force_ball_val = 0

while True:
    if keyboard_mode:
        paddle.steer_with_keyboard(p.readUserDebugParameter(rotation_speed_id))
    else:
        paddle.read_and_update_joint_position()

    # Check if the reset button was clicked, and reset the ball eventually.
    if p.readUserDebugParameter(reset_ball_button) > reset_ball_val:
        reset_ball_val = p.readUserDebugParameter(reset_ball_button)
        p.resetBasePositionAndOrientation(ball, [0.15, 0, 1], [0, 0, 0, 1])

    # Check if the force button was clicked, and throw the ball eventually.
    if p.readUserDebugParameter(force_ball_button) > force_ball_val:
        force_ball_val = p.readUserDebugParameter(force_ball_button)
        curr_ball = p.getBasePositionAndOrientation(ball)[0]
        curr_paddle = paddle.get_center_position()
        vec = utils.sub_vertices(curr_paddle, curr_ball)
        vec = utils.scale_vector(vec)
        p.applyExternalForce(ball, -1, vec, [0, 0, 0], p.WORLD_FRAME)

    p.stepSimulation()

    time.sleep(0.01)  # sometimes pybullet crashes, this line helps a lot
