import time
from collections import deque
import pybullet as p

from utils.environment import init_env_and_load_assets, update_wind_controllers
from utils.pid_performer import PidPerformer

ball_controller, ball, paddle, wind_controllers = init_env_and_load_assets(p)

paddle.create_joint_controllers()
pid_performer = PidPerformer(p, ball, paddle)


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
