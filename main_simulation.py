#!/usr/bin/env python3
import argparse
import time

import pybullet as p

from position_prediction.physical_prediction import PhysicalPredictier
from trackers.ball_tracker import BallTracker
from utils.environment import (
    init_env_and_load_assets,
    update_wind_controllers,
    update_force_controllers,
)
from utils.pid_performer import PidPerformer


def get_mode():
    parser = argparse.ArgumentParser(description="Mode manager")

    parser.add_argument("--mode", dest="mode", type=str, help="Steering mode.")
    parser.add_argument("--pid", action="store_true")
    args = parser.parse_args()

    return args.mode, args.pid


mode, pid_flag = get_mode()
keyboard_mode = mode == "keyboard"

(
    ball_controller,
    ball,
    paddle,
    wind_controllers,
    force_controllers,
) = init_env_and_load_assets(p)

if keyboard_mode:
    # add rotation speed controller
    rotation_speed_id = p.addUserDebugParameter("rotation_speed", 0, 45, 5)
    paddle.move_by_vector([0, 0, 0.5])
else:
    paddle.create_joint_controllers()

if pid_flag:
    pid_performer = PidPerformer(p, BallTracker(ball, paddle), paddle)

predicter = PhysicalPredictier(ball, paddle)


p.setTimeStep(0.01)


for _ in range(1000):

    start_time = time.time()
    if not paddle.check_if_in_range(ball.get_position()):
        break

    if keyboard_mode:
        paddle.steer_with_keyboard(p.readUserDebugParameter(rotation_speed_id))
    else:
        paddle.read_and_update_joint_position()

    print("Adding position", ball.get_position()[:2])
    predicter.add_position(ball.get_position())
    print("\nNEXT POSITION PREDICTION")
    print("predicted = ", predicter.next_position())
    print("---------------------------------------------")

    if pid_flag:
        pid_performer.perform_pid_step()

    ball_controller.check_and_update_rotation()
    ball_controller.check_if_drop_with_rotation()
    if ball_controller.should_throw_ball():
        ball_controller.throw_ball(paddle.get_center_position())

    update_wind_controllers(p, *wind_controllers)
    update_force_controllers(p, ball, *force_controllers)

    p.stepSimulation()

    # TODO ten sleep powinien być długości częstotliwości symulacji.
    # stepSimulation will perform all the actions in a single forward dynamics
    # simulation step such as collision detection, constraint solving and integration.
    # The default timestep is 1/240 second, it can be changed using the setTimeStep or setPhysicsEngineParameter API.
    time.sleep(max(0, 0.01 - (time.time() - start_time)))
    # sometimes pybullet crashes, this line helps a lot

    # [597.7266677411063, -916.5698238987555, 3459.2698871845996]

predicter.debug_plot()
