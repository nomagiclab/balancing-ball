import argparse
import os

from position_prediction.benchmark import Benchmark
import pybullet as p

from trackers.ball_tracker import BallTracker
from utils.environment import init_env_and_load_assets

parser = argparse.ArgumentParser()
DEFAULT_FILE_NAME = "polynomial_prediction_benchmark"

parser.add_argument("--file_name", default=DEFAULT_FILE_NAME, type=str)
parser.add_argument("--plot_only", action="store_true")
parser.add_argument("--wind_tests", action="store_true")
args = parser.parse_args()

file_name = args.file_name
csv_name = file_name + ".csv"
plot_name = file_name + ".png"

if args.plot_only:
    Benchmark.plot_error(csv_name, plot_name)
else:
    (
        ball_controller,
        ball,
        paddle,
        wind_controllers,
        force_controllers,
    ) = init_env_and_load_assets(p)

    paddle.create_joint_controllers()

    tracker = BallTracker(ball, paddle)
    paddle.create_joint_controllers()

    benchmark = Benchmark(tracker, ball, csv_name, TESTS_WIND=[(-1.1, 0.8)], FORCE_TESTS=[(0.3, 0.3, 0)])
    if args.wind_tests:
        benchmark.run_benchmark(p, paddle, 35.0)
    else:
        benchmark.run_force_benchmark(p, paddle)

    benchmark.plot_error(csv_name, plot_name)

    #os.remove(csv_name)
    #os.remove(plot_name)
