import time
from collections import deque
import pybullet as p

from ball.delayed_pybullet_ball import DelayedPybulletBall
from position_prediction.polynomial_interpolation import PolynomialPredicter
from trackers.concurrent_ball_tracker import ConcurrentPredictingBallTracker
from trackers.predicting_ball_tracker import PredictingBallTracker
from utils.environment import init_env_and_load_assets, update_wind_controllers
from utils.pid_performer import PidPerformer

ball_controller, ball, paddle, wind_controllers = init_env_and_load_assets(p)

paddle.create_joint_controllers()

N_DELAYED = 10
N_PREDICT = 15

predicter = PolynomialPredicter(N_PREDICT)
tracker = ConcurrentPredictingBallTracker(ball, paddle, predicter, 0.05)
pid_performer = PidPerformer(p, tracker, paddle)

while True:
    paddle.read_and_update_joint_position()

    pid_performer.perform_pid_step()

    ball_controller.check_and_update_rotation()
    ball_controller.check_if_drop_with_rotation()

    if ball_controller.should_throw_ball():
        ball_controller.throw_ball(paddle.get_center_position())

    update_wind_controllers(p, *wind_controllers)

    p.stepSimulation()

    time.sleep(0.01)  # sometimes pybullet crashes, this line helps a lot
