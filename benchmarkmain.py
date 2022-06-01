import argparse
import os

import pybullet as p

from ball.delayed_pybullet_ball import DelayedPybulletBall
from benchmarks.stpos_benchmark import StPosBenchmark
from benchmarks.wind_benchmark import WindBenchmark
from position_prediction.DES import DESPredicter
from benchmarks.force_benchmark import ForceBenchmark
from position_prediction.no_prediction import NoPredictionPredicter
from trackers.concurrent_ball_tracker import ConcurrentPredictingBallTracker
from utils.environment import init_env_and_load_assets

parser = argparse.ArgumentParser()
DEFAULT_FILE_NAME = "prediction_error"
DEFAULT_N_PREDICT = 1
DEFAULT_N_DELAYED = 0
DEFAULT_FETCH_TIME = 1 / 30  # 20 is the maximum number of camera outputs per second.


parser.add_argument("--file_name", default=DEFAULT_FILE_NAME, type=str)
parser.add_argument(
    "-d", type=int, help="N_DELAYED parameter", default=DEFAULT_N_DELAYED
)
parser.add_argument(
    "--benchmark-type", type=str, help="Specify the benchmark type.", default="FORCE"
)
parser.add_argument(
    "-p", type=int, help="N_PREDICT parameter", default=DEFAULT_N_PREDICT
)
parser.add_argument(
    "-f", type=float, help="FETCH_TIME parameter", default=DEFAULT_FETCH_TIME
)
parser.add_argument(
    "--no-prediction", help="USE no_prediciton predicter", action="store_true"
)
parser.add_argument("--delete", action="store_true")
args = parser.parse_args()

N_DELAYED = args.d
N_PREDICT = args.p
FETCH_TIME = args.f
NO_PREDICTION = args.no_prediction
BENCHMARK_TYPE = args.benchmark_type
(
    ball_controller,
    ball,
    paddle,
    wind_controllers,
    force_controllers,
) = init_env_and_load_assets(p)

paddle.create_joint_controllers()

if NO_PREDICTION:
    predicter = NoPredictionPredicter()
else:
    predicter = DESPredicter(1)

tracker = ConcurrentPredictingBallTracker(
    DelayedPybulletBall(ball, N_DELAYED), paddle, predicter, FETCH_TIME
)

file_name = args.file_name
csv_name = file_name + ".csv"
plot_name = file_name + ".png"

if BENCHMARK_TYPE == "POSITION":
    benchmark = StPosBenchmark(tracker, ball)
elif BENCHMARK_TYPE == "WIND":
    benchmark = WindBenchmark(tracker, ball)
else:
    benchmark = ForceBenchmark(tracker, ball, [(0.225, 0.225), (0.1, 0.1), (-0.2, 0.1)])

benchmark.run_benchmark(p, paddle, 3, (400.0, 1.0, 70.0))

print("SAVING PLOTS")

if BENCHMARK_TYPE == "FORCE":
    benchmark.get_prediction_error(plot_name)

benchmark.plot()
input("CONTINUE?")

if args.delete:
    os.remove(csv_name)
    os.remove(plot_name)
