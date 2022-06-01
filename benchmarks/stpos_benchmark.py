import time
from typing import List, Tuple

import pybullet

import ball.pybullet_ball as pybullet_ball
from ball.pybullet_ball import PyBulletBall
from paddle.paddle import Paddle
from plotting.plot_maker import PlotMaker
from trackers.abstract_tracker import AbstractBallTracker, OutOfRange
from trackers.ball_tracker import BallTracker
from utils.pid_performer import PidPerformer

BALL_RADIUS = 0.03


class StPosBenchmark:
    DEFAULT_POSES = [
        (0.07, 0, BALL_RADIUS),
        (0, 0.05, BALL_RADIUS),
        (-0.07, 0.05, BALL_RADIUS),
        (0.035, -0.06, BALL_RADIUS),
    ]

    PYBULLET_TIME_STEP = 1 / 100

    def __init__(
        self,
        tracker: AbstractBallTracker,
        ball: PyBulletBall,
        pose_tests: List[Tuple[float, float]] = None,
    ):
        if pose_tests is None:
            pose_tests = StPosBenchmark.DEFAULT_POSES

        self.tracker = tracker
        self.ball = ball
        self.pose_tests = pose_tests
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

    def run_benchmark(
        self,
        pybullet_client: pybullet,
        paddle: Paddle,
        test_time_period=5.0,
        pid_parameters=None,
    ):
        if pid_parameters is None:
            pid_parameters = [1, 0.1, 1]

        pybullet_client.setTimeStep(self.PYBULLET_TIME_STEP)

        self.pose_tests.insert(0, (0.0, 0.0, 1.0))

        for p_test in self.pose_tests:
            pid_performer = PidPerformer(
                pybullet_client, self.tracker, paddle, *pid_parameters
            )
            self.ball.set_position(
                [x + y for x, y in zip(p_test, paddle.get_center_position())],
                pybullet_ball.DEFAULT_ORIENTATION,
            )

            if self._perform_test(
                pybullet_client, paddle, pid_performer, test_time_period
            ):
                print("BENCHMARK FAILED")
                break

    def plot(self):
        self.plotter.plot_subplots(
            [["Error on x axis"], ["Error on y axis"]],
            "Ball positions",
            ["Error on x axis", "Error on y axis"],
        )
