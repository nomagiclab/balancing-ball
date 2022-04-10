from position_prediction.benchmark import Benchmark
import pybullet as p

from ball.delayed_pybullet_ball import DelayedPybulletBall
from position_prediction.polynomial_interpolation import PolynomialPredicter
from trackers.concurrent_ball_tracker import ConcurrentPredictingBallTracker
from utils.environment import init_env_and_load_assets

ball_controller, ball, paddle, wind_controllers = init_env_and_load_assets(p)

paddle.create_joint_controllers()

N_DELAYED = 3
N_PREDICT = 20

predicter = PolynomialPredicter()
tracker = ConcurrentPredictingBallTracker(
    DelayedPybulletBall(ball, N_DELAYED), paddle, N_PREDICT, 0, predicter, 0.05
)

file_name = "polynomial_prediction_benchmark.csv"

benchmark = Benchmark(tracker, ball, file_name)
benchmark.run_benchmark(p, paddle)

benchmark.plot_linear(file_name)
