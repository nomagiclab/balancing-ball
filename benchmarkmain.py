from position_prediction.benchmark import Benchmark
import pybullet as p

from ball.delayed_pybullet_ball import DelayedPybulletBall
from position_prediction.polynomial_interpolation import PolynomialPredicter
from trackers.concurrent_ball_tracker import ConcurrentPredictingBallTracker
from utils.environment import init_env_and_load_assets

ball_controller, ball, paddle, wind_controllers = init_env_and_load_assets(p)

paddle.create_joint_controllers()

N_DELAYED = 0
N_PREDICT = 1

predicter = PolynomialPredicter()
tracker = ConcurrentPredictingBallTracker(
    DelayedPybulletBall(ball, N_DELAYED), paddle, N_PREDICT, 0, predicter, 0.0001
)

FILE_NAME = "polynomial_prediction_benchmark"
file_name = FILE_NAME + ".csv"
plot_name = FILE_NAME + ".png"

benchmark = Benchmark(tracker, ball, file_name, [(1.5, 1.5), (-1.5, -1.5)])
benchmark.run_benchmark(p, paddle, 6)

benchmark.plot_linear(file_name, plot_name)
