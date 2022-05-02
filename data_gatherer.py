#!/usr/bin/env python3
import argparse
import time


import pybullet as p
import pandas as pd
import numpy as np


from trackers.ball_tracker import BallTracker
from utils.environment import init_minimalistic_env_and_load_assets
from utils.pid_performer import PidPerformer

INITIAL_WAIT_TIME = 3.0
DEFAULT_FETCH_TIME = 0.1
RANDOM_EVENT_TIME = 0.2
DEFAULT_TRIAL_NUM = 5


parser = argparse.ArgumentParser(description="Mode manager")
parser.add_argument("--pid", action="store_true")
parser.add_argument("--filename", action="store", type=str, default="gathered_data.csv")
parser.add_argument(
    "--fetch_time", action="store", type=float, default=DEFAULT_FETCH_TIME
)
parser.add_argument(
    "--initial_wait_time", action="store", type=float, default=INITIAL_WAIT_TIME
)
parser.add_argument(
    "--random_event_time", action="store", type=float, default=RANDOM_EVENT_TIME
)
parser.add_argument(
    "--number_of_trials", action="store", type=int, default=DEFAULT_TRIAL_NUM
)
args = parser.parse_args()
filename = args.filename
pid_flag = args.pid
fetch_time = args.fetch_time
initial_wait_time = args.initial_wait_time
random_event_time = args.random_event_time
trial_num = args.number_of_trials

(ball, paddle) = init_minimalistic_env_and_load_assets(p)


paddle.create_joint_controllers()

if pid_flag:
    pid_performer = PidPerformer(p, BallTracker(ball, paddle), paddle)

initial_wait_timer = time.time()
fetch_timer = time.time()
random_event_timer = time.time()


def distance_from_paddle_center(pos):
    return np.linalg.norm(np.asarray(pos) - np.asarray([0.0, 0.0, 0.5]), ord=2)


def vector_norm(vec):
    return np.linalg.norm(np.asarray(vec), ord=2)


trial_id = 0
df = pd.DataFrame(
    columns=[
        "trial_id",
        "pos_x",
        "pos_y",
        "pos_z",
        "lin_x",
        "lin_y",
        "lin_z",
        "ang_x",
        "ang_y",
        "ang_z",
        "y_roll",
        "x_roll",
    ]
)

while True:
    paddle.read_and_update_joint_position()
    if time.time() - initial_wait_timer >= initial_wait_time:
        if time.time() - fetch_timer >= fetch_time:
            linear_velocity, angular_velocity = ball.get_velocity()
            position = ball.get_position()
            _, y_joint_state, x_joint_state = paddle.get_joint_rolls()
            # rolls are at index 0 in those tuples - see pybullet documentation for further details
            y_roll, x_roll = y_joint_state[0], x_joint_state[0]

            df.loc[len(df)] = [
                trial_id,
                *position,
                *linear_velocity,
                *angular_velocity,
                y_roll,
                x_roll,
            ]
            fetch_timer = time.time()

        if pid_flag:
            pid_performer.perform_pid_step()

        if time.time() - random_event_timer >= random_event_time:
            linear_velocity, angular_velocity = ball.get_velocity()
            if (
                vector_norm(linear_velocity) + vector_norm(angular_velocity) < 0.5
                and distance_from_paddle_center(ball.get_position()) < 0.2
            ):
                random_angular_velocity = np.random.uniform(
                    low=-0.3, high=0.3, size=3
                ).tolist()
                random_linear_velocity = np.random.uniform(
                    low=-0.7, high=0.7, size=3
                ).tolist()
                ball.set_ball_velocity(random_linear_velocity, random_angular_velocity)

            random_event_timer = time.time()

        if distance_from_paddle_center(ball.get_position()) > 0.4:
            ball.stabilize_ball()
            ball.set_position([0, 0, 0.5 + 0.1], ball.get_orientation())
            # setting new trial id
            trial_id += 1
            if trial_id == trial_num:
                break
            # delaying random event occurence
            random_event_timer = time.time()
    p.stepSimulation()

    time.sleep(0.01)  # sometimes pybullet crashes, this line helps a lot

df.to_csv(filename, sep=",")
print("DATA GATHERED TO:", filename)
