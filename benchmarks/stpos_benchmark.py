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
    DEFAULT_POSE = [0.07, 0]

    INITIAL_WAIT_TIME = 2

    PYBULLET_TIME_STEP = 1 / 100

    def __init__(
        self,
        tracker: AbstractBallTracker,
        ball: PyBulletBall,
        pose_test: Tuple[float, float] = None,
    ):
        if pose_test is None:
            pose_test = StPosBenchmark.DEFAULT_POSE
        pose_test.append(BALL_RADIUS)

        self.tracker = tracker
        self.ball = ball
        self.pose_test = pose_test
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

    def run_idle_simulation(self, pybullet_client, wait_time: float):
        start_time = time.time()
        while time.time() - start_time < wait_time:
            loop_time = time.time()
            pybullet_client.stepSimulation()
            time.sleep(max(self.PYBULLET_TIME_STEP - (time.time() - loop_time), 0))

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

        pid_performer = PidPerformer(
            pybullet_client, self.tracker, paddle, *pid_parameters
        )

        paddle.read_and_update_joint_position()
        self.run_idle_simulation(pybullet_client, self.INITIAL_WAIT_TIME)

        self.ball.set_position(
            [x + y for x, y in zip(self.pose_test, paddle.get_center_position())],
            pybullet_ball.DEFAULT_ORIENTATION,
        )

        if not self._perform_test(
            pybullet_client, paddle, pid_performer, test_time_period
        ):
            print("BENCHMARK FAILED")

    def plot(self):
        self.plotter.plot_subplots(
            [["Error on x axis"], ["Error on y axis"]],
            "Ball positions",
            ["Error on x axis", "Error on y axis"],
        )
