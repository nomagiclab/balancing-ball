import time
from typing import Tuple

import pybullet

from ball.pybullet_ball import PyBulletBall
from paddle.paddle import Paddle
from plotting.plot_maker import PlotMaker
from trackers.abstract_tracker import AbstractBallTracker
from utils.environment import set_wind, apply_force
from utils.pid_performer import PidPerformer


class ForceBenchmark:
    # Time it takes for ball_id to stabilize.
    # INITIAL_WAIT_TIME = 5.0

    DEFAULT_FORCES = [
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
        tests_forces=None,
    ):
        if tests_forces is None:
            tests_forces = self.DEFAULT_FORCES
        self.tracker = tracker
        self.ball = ball
        self.tests_forces = tests_forces
        self.plotter = PlotMaker(["Error on x axis", "Error on y axis"])

    def run_benchmark(
        self,
        pybullet_client: pybullet,
        paddle: Paddle,
        force_period_length=5.0,
        pid_params: Tuple[float, float, float] = (100, 1, 300),
    ):
        test_start = time.time()

        pybullet_client.setTimeStep(self.PYBULLET_TIME_STEP)

        pid_performer = PidPerformer(pybullet_client, self.tracker, paddle, *pid_params)

        benchmark_failed = False

        self.tests_forces.insert(0, (0, 0))

        for test_force in self.tests_forces:
            apply_force(pybullet_client, self.ball.id, *test_force)
            time_left = force_period_length

            while not benchmark_failed and time_left > 0:
                start_time = time.time()

                if not paddle.check_if_in_range(self.ball.get_position()):
                    print("Benchmark failed, ball_id out of range!")
                    benchmark_failed = True

                paddle.read_and_update_joint_position()
                pid_performer.perform_pid_step()

                t = time.time()
                error = self.tracker.get_error_vector()
                self.plotter.add("Error on x axis", t - test_start, error[0])
                self.plotter.add("Error on y axis", t - test_start, error[1])

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
            ["error [cm]", "error [cm]"],
        )
