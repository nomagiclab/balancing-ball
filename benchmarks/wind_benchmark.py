import time

import pybullet

from ball.pybullet_ball import PyBulletBall
from paddle.paddle import Paddle
from plotting.plot_maker import PlotMaker
from trackers.abstract_tracker import AbstractBallTracker, OutOfRange
from trackers.ball_tracker import BallTracker
from utils.environment import set_wind
from utils.pid_performer import PidPerformer


class WindBenchmark:
    # Time it takes for ball to stabilize.
    # INITIAL_WAIT_TIME = 5.0

    DEFAULT_TESTS_WIND = [
        (-1.5, 0.0),
        (1.5, 0.0),
        (0.0, 1.5),
        (0.0, -1.5),
        (0.9, 0.9),
        (-0.9, 0.9),
        (-0.9, -0.9),
        (0.9, -0.9),
    ]

    PYBULLET_TIME_STEP = 1 / 100

    def __init__(
        self,
        tracker: AbstractBallTracker,
        ball: PyBulletBall,
        tests_wind=None,
    ):
        if tests_wind is None:
            tests_wind = self.DEFAULT_TESTS_WIND
        self.tracker = tracker
        self.ball = ball
        self.tests_wind = tests_wind
        self.plotter = PlotMaker(["Error on x axis", "Error on y axis"])

    def _perform_test(self, pybullet_client, paddle, pid_performer, test_time_period):
        real_tracker = BallTracker(self.ball, paddle)
        time_left = test_time_period

        while time_left > 0:
            start_time = time.time()
            paddle.read_and_update_joint_position()
            pid_performer.perform_pid_step()

            t = time.time()

            try:
                error = real_tracker.get_error_vector()
                self.plotter.add("Error on x axis", t, error[0])
                self.plotter.add("Error on y axis", t, error[1])
            except OutOfRange:
                return False

            pybullet_client.stepSimulation()
            time.sleep(max(self.PYBULLET_TIME_STEP - (time.time() - start_time), 0))
            time_left -= time.time() - start_time

        return True

    def run_benchmark(
        self,
        pybullet_client: pybullet,
        paddle: Paddle,
        wind_period_length=5.0,
        pid_parameters=None,
    ):
        if pid_parameters is None:
            pid_parameters = [1, 0.1, 1]

        pybullet_client.setTimeStep(self.PYBULLET_TIME_STEP)

        pid_performer = PidPerformer(
            pybullet_client, self.tracker, paddle, *pid_parameters
        )

        self.tests_wind.insert(0, (0, 0))

        for test_wind in self.tests_wind:
            set_wind(pybullet_client, *test_wind)

            if self._perform_test(
                pybullet_client, paddle, pid_performer, wind_period_length
            ):
                print("BENCHMARK FAILED")
                break

    def plot(self):
        self.plotter.plot_subplots(
            [["Error on x axis"], ["Error on y axis"]],
            "Ball positions",
            ["Error on x axis", "Error on y axis"],
            ["error [m]", "error [m]"],
        )
