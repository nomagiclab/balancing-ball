import argparse
import os

from position_prediction.benchmark import Benchmark
import pybullet as p

from ball.delayed_pybullet_ball import DelayedPybulletBall
from position_prediction.polynomial_interpolation import PolynomialPredicter
from trackers.concurrent_ball_tracker import ConcurrentPredictingBallTracker
from utils.environment import init_env_and_load_assets

parser = argparse.ArgumentParser()
DEFAULT_FILE_NAME = "polynomial_prediction_benchmark"

DEFAULT_N_PREDICT = 10
DEFAULT_FETCH_TIME = 1 / 20  # 20 is the maximum number of camera outputs per second.

parser.add_argument("--file_name", default=DEFAULT_FILE_NAME, type=str)
parser.add_argument(
    "-d", type=int, help="N_DELAYED parameter", default=DEFAULT_N_PREDICT
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

file_name = args.file_name
csv_name = file_name + ".csv"
plot_name = file_name + ".png"

benchmark = Benchmark(tracker, ball, csv_name, [(0.5, 0.5), (-0.5, -0.5), (-1, -1)])
benchmark.run_benchmark(p, paddle, 6)

benchmark.plot_linear(csv_name, plot_name)

if args.delete:
    os.remove(csv_name)
    os.remove(plot_name)
