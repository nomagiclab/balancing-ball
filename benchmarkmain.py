import argparse
import os

import pybullet as p

from ball.delayed_pybullet_ball import DelayedPybulletBall
from benchmarks.force_benchmark import ForceBenchmark
from position_prediction.polynomial_interpolation import PolynomialPredicter
from trackers.ball_tracker import BallTracker
from trackers.concurrent_ball_tracker import ConcurrentPredictingBallTracker
from utils.environment import init_env_and_load_assets

parser = argparse.ArgumentParser()
DEFAULT_FILE_NAME = "polynomial_prediction_benchmark"
DEFAULT_N_PREDICT = 1
DEFAULT_N_DELAYED = 0
DEFAULT_FETCH_TIME = 1 / 60  # 20 is the maximum number of camera outputs per second.

parser.add_argument("--file_name", default=DEFAULT_FILE_NAME, type=str)
parser.add_argument(
    "-d", type=int, help="N_DELAYED parameter", default=DEFAULT_N_DELAYED
)
parser.add_argument(
    "-p", type=int, help="N_PREDICT parameter", default=DEFAULT_N_PREDICT
)
parser.add_argument(
    "-f", type=float, help="FETCH_TIME parameter", default=DEFAULT_FETCH_TIME
)
parser.add_argument("--delete", action="store_true")
args = parser.parse_args()

N_DELAYED = args.d
N_PREDICT = args.p
FETCH_TIME = args.f

(
    ball_controller,
    ball,
    paddle,
    wind_controllers,
    force_controllers,
) = init_env_and_load_assets(p)

paddle.create_joint_controllers()

predicter = PolynomialPredicter(N_PREDICT)
tracker = ConcurrentPredictingBallTracker(
    DelayedPybulletBall(ball, N_DELAYED), paddle, predicter, FETCH_TIME
)


# tracker = BallTracker(ball, paddle)

file_name = args.file_name
csv_name = file_name + ".csv"
plot_name = file_name + ".png"

benchmark = ForceBenchmark(tracker, ball, [(0.17, 0.17), (0.1, 0.1), (-0.2, 0.1)])
benchmark.run_benchmark(p, paddle, 3, (300.0, 1.0, 100.0))

benchmark.plot()

if args.delete:
    os.remove(csv_name)
    os.remove(plot_name)
