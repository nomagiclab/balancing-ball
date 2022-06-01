import time
from typing import Tuple

import pybullet

from ball.pybullet_ball import PyBulletBall
from paddle.paddle import Paddle
from plotting.plot_maker import PlotMaker
from trackers.abstract_tracker import AbstractBallTracker, OutOfRange
from trackers.ball_tracker import BallTracker
from utils.environment import set_wind, apply_force
from utils.pid_performer import PidPerformer

import pandas
from datetime import date
import csv


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
        csv_file_name: str = None,
    ):
        if tests_forces is None:
            tests_forces = self.DEFAULT_FORCES
        self.tracker = tracker
        self.ball = ball
        self.tests_forces = tests_forces
        self.plotter = PlotMaker(["Error on x axis", "Error on y axis"])
        if csv_file_name is None:
            csv_file_name = "benchmark" + date.today().strftime("%b-%d-%Y") + ".csv"
        self.csv_file_name = csv_file_name
        self.csv_file = open(self.csv_file_name, "w")
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(["Frame", "X", "Y", "Z", "X_pred", "Y_pred", "Z_pred"])

        self.average_error = (0, 0, 0)
        self.frame = 0

    def _write_info(self):
        predicted_pos = self.tracker.last_predicted_pos

        if predicted_pos is not None:
            real_pos = self.ball.get_position()

            self.csv_writer.writerow([self.frame, *real_pos, *predicted_pos])

            self.average_error = tuple(
                self.average_error[i] + abs(predicted_pos[i] - real_pos[i])
                for i in range(3)
            )

        self.frame += 1

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

            self._write_info()

            pybullet_client.stepSimulation()
            time.sleep(max(self.PYBULLET_TIME_STEP - (time.time() - start_time), 0))
            time_left -= time.time() - start_time

        return True

    def run_benchmark(
        self,
        pybullet_client: pybullet,
        paddle: Paddle,
        force_period_length=5.0,
        pid_params: Tuple[float, float, float] = (100, 1, 300),
    ):
        pybullet_client.setTimeStep(self.PYBULLET_TIME_STEP)

        pid_performer = PidPerformer(pybullet_client, self.tracker, paddle, *pid_params)

        self.tests_forces.insert(0, (0, 0))

        for test_force in self.tests_forces:
            apply_force(pybullet_client, self.ball.id, *test_force)

            if not self._perform_test(
                pybullet_client, paddle, pid_performer, force_period_length
            ):
                print("BENCHMARK FAILED")
                break

        self.csv_file.close()

    def plot(self):
        self.plotter.plot_subplots(
            [["Error on x axis"], ["Error on y axis"]],
            "Ball positions",
            ["Error on x axis", "Error on y axis"],
            ["error [cm]", "error [cm]"],
        )

    def get_prediction_error(self, plot_file_name):
        self.plot_linear(self.csv_file_name, plot_file_name)

    @staticmethod
    def plot_error(csv_file_name: str, plot_filename: str):
        from matplotlib import pyplot as plt

        data = pandas.read_csv(csv_file_name)
        fig, axs = plt.subplots(2)
        fig.suptitle("Ball positions")
        fig.tight_layout()

        axs[0].set_title("Error on x axis")
        axs[0].plot(data["Frame"], data["X"], label="X", color="red")
        axs[1].set_title("Error on y axis")
        axs[1].plot(data["Frame"], data["Y"], label="Y", color="green")
        plt.savefig(plot_filename)

    @staticmethod
    def plot_linear(csv_file_name: str, plot_file_name):
        from matplotlib import pyplot as plt

        data = pandas.read_csv(csv_file_name)
        fig, axs = plt.subplots(3, constrained_layout=True)
        fig.suptitle("Prediction errors")

        axs[0].set_title("Error on x axis")
        axs[0].set_ylabel("error [cm]")
        axs[0].plot(
            data["Frame"], abs(data["X_pred"] - data["X"]), label="X", color="red"
        )
        axs[1].set_title("Error on y axis")
        axs[1].set_ylabel("error [cm]")
        axs[1].plot(
            data["Frame"], abs(data["Y_pred"] - data["Y"]), label="Y", color="green"
        )
        axs[2].set_title("Distance (sqrt(x^2 + y^2))")
        axs[2].set_ylabel("error [cm]")
        axs[2].plot(
            data["Frame"],
            ((data["Y_pred"] - data["Y"]) ** 2 + (data["X_pred"] - data["X"]) ** 2)
            ** (0.5),
            label="error",
            color="blue",
        )
        plt.savefig(plot_file_name)
