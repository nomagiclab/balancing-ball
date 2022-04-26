import time

import pybullet as p

from position_prediction.physical_prediction import PhysicalPredictier
from trackers.concurrent_ball_tracker import ConcurrentPredictingBallTracker
from utils.environment import (
    init_env_and_load_assets,
    update_force_controllers,
    update_wind_controllers,
)
from utils.pid_performer import PidPerformer

(
    ball_controller,
    ball,
    paddle,
    wind_controllers,
    force_controllers,
) = init_env_and_load_assets(p)

PYBULLET_TIME_STEP = 0.01

p.setTimeStep(PYBULLET_TIME_STEP)
paddle.create_joint_controllers()

FETCH_TIME = 1 / 20

predicter = PhysicalPredictier(ball, paddle)
tracker = ConcurrentPredictingBallTracker(ball, paddle, predicter, FETCH_TIME)
pid_performer = PidPerformer(p, tracker, paddle)

for _ in range(2000):
    start_time = time.time()

    paddle.read_and_update_joint_position()

    pid_performer.perform_pid_step()

    ball_controller.check_and_update_rotation()
    ball_controller.check_if_drop_with_rotation()

    if ball_controller.should_throw_ball():
        ball_controller.throw_ball(paddle.get_center_position())

    update_wind_controllers(p, *wind_controllers)

    update_force_controllers(p, ball, *force_controllers)

    p.stepSimulation()

    time.sleep(max(0.0, PYBULLET_TIME_STEP - (time.time() - start_time)))

predicter.debug_plot()
