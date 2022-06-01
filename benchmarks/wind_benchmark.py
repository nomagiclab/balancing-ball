import time

import pybullet

from ball.pybullet_ball import PyBulletBall
from paddle.paddle import Paddle
from plotting.plot_maker import PlotMaker
from trackers.abstract_tracker import AbstractBallTracker
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

    def run_benchmark(
        self, pybullet_client: pybullet, paddle: Paddle, wind_period_length=5.0
    ):

        pybullet_client.setTimeStep(self.PYBULLET_TIME_STEP)

        pid_performer = PidPerformer(pybullet_client, self.tracker, paddle)

        benchmark_failed = False

        self.tests_wind.insert(0, (0, 0))

        for test_wind in self.tests_wind:
            set_wind(pybullet_client, *test_wind)
            time_left = wind_period_length

            while not benchmark_failed and time_left > 0:
                start_time = time.time()

                if not paddle.check_if_in_range(self.ball.get_position()):
                    print("Benchmark failed, ball out of range!")
                    benchmark_failed = True

                paddle.read_and_update_joint_position()
                pid_performer.perform_pid_step()

                t = time.time()
                error = self.tracker.get_error_vector()
                self.plotter.add("Error on x axis", t, error[0])
                self.plotter.add("Error on y axis", t, error[1])

                pybullet_client.stepSimulation()
                time.sleep(max(self.PYBULLET_TIME_STEP - (time.time() - start_time), 0))
                time_left -= time.time() - start_time

            if benchmark_failed:
                break

        if benchmark_failed:
            print("BENCHMARK FAILED")
        return

    def plot(self):
        self.plotter.plot_subplots(
            [["Error on x axis"], ["Error on y axis"]],
            "Ball positions",
            ["Error on x axis", "Error on y axis"],
        )
