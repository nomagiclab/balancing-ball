import csv
import time
from datetime import date

import pandas
import pybullet

import ball.pybullet_ball as pybullet_ball
from ball.pybullet_ball import PyBulletBall
from paddle.paddle import Paddle
from trackers.abstract_tracker import AbstractBallTracker
from utils.environment import set_wind
from utils.pid_performer import PidPerformer
import matplotlib as plt
from typing import List


def _perform_sim_step(p: pybullet, paddle, pid_performer: PidPerformer):
    paddle.read_and_update_joint_position()
    pid_performer.perform_pid_step()
    p.stepSimulation()
    time.sleep(0.01)


class Benchmark:
    # Time it takes for ball to stabilize.
    INITIAL_WAIT_TIME = 5.0

    DEFAULT_BALL_POSITION = [0, 0, 0.7]

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

    def __init__(
        self,
        tracker: AbstractBallTracker,
        ball: PyBulletBall,
        csv_file_name: str = None,
        TESTS_WIND=None,
        FORCE_TESTS=None,
    ):
        if TESTS_WIND is None:
            TESTS_WIND = self.DEFAULT_TESTS_WIND

        self.force_tests = FORCE_TESTS

        assert hasattr(tracker, "last_predicted_pos")

        self.tracker = tracker
        self.ball = ball
        self.TESTS_WIND = TESTS_WIND

        if csv_file_name is None:
            csv_file_name = "benchmark" + date.today().strftime("%b-%d-%Y") + ".csv"

        self.csv_file_name = csv_file_name
        self.csv_file = open(self.csv_file_name, "w")
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(["Frame", "X", "Y", "Z", "X_pred", "Y_pred", "Z_pred"])

        self.average_error = (0, 0, 0)
        self.frame = 0

    def _reset_test_data(self):
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

    def print_results(self):
        print(
            "Average error (x, y, z): "
            + str(tuple(self.average_error[i] / self.frame for i in range(3)))
        )

    def run_force_benchmark(self, p: pybullet, paddle):
        MAX_TEST_TIME = 25.0
        pid_performer = PidPerformer(p, self.tracker, paddle)
        self._reset_test_data()

        for test in self.force_tests:
            self.ball.set_position(
                self.DEFAULT_BALL_POSITION, pybullet_ball.DEFAULT_ORIENTATION
            )
            start_time = time.time()
            while time.time() - start_time < self.INITIAL_WAIT_TIME / 2:
                self._write_info()
                _perform_sim_step(p, paddle, pid_performer)

            p.applyExternalForce(self.ball.id, -1, test, [0, 0, 0], p.WORLD_FRAME)
            start_time = time.time()

            while True:
                if not paddle.check_if_in_range(self.ball.get_position()):
                    print("Benchmark failed, ball out of range! FORCE: ", test)
                    break

                if time.time() - start_time > MAX_TEST_TIME:
                    break
                self._write_info()
                _perform_sim_step(p, paddle, pid_performer)

    def run_benchmark(
        self, pybullet_client: pybullet, paddle: Paddle, wind_period_length=5.0
    ):
        pid_performer = PidPerformer(pybullet_client, self.tracker, paddle)

        test = -1
        time_left = self.INITIAL_WAIT_TIME
        last_time = time.time()

        PYBULLET_TIME_STEP = 1 / 100

        while True:
            start_time = time.time()
            if not paddle.check_if_in_range(self.ball.get_position()):
                print("Benchmark failed, ball out of range!")
                self.print_results()
                break

            if time_left <= 0.0:
                test += 1

                if test >= len(self.TESTS_WIND):
                    print("Benchmark finished!")
                    self.print_results()
                    break

                set_wind(pybullet_client, *self.TESTS_WIND[test])
                time_left = wind_period_length

            self._write_info()
            _perform_sim_step(pybullet_client, paddle, pid_performer)

            time_left -= time.time() - last_time
            last_time = time.time()

            pybullet_client.stepSimulation()
            time.sleep(PYBULLET_TIME_STEP - (time.time() - start_time))

        self.csv_file.close()

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
        fig, axs = plt.subplots(3)
        fig.suptitle("Prediction errors")
        fig.tight_layout()

        axs[0].set_title("Error x")
        axs[0].plot(
            data["Frame"], abs(data["X_pred"] - data["X"]), label="X", color="red"
        )
        axs[1].set_title("Error y")
        axs[1].plot(
            data["Frame"], abs(data["Y_pred"] - data["Y"]), label="Y", color="green"
        )
        axs[2].set_title("Squared error (x^2 + y^2)")
        axs[2].plot(
            data["Frame"],
            abs(data["Y_pred"] - data["Y"]) ** 2 + abs(data["X_pred"] - data["X"]) ** 2,
            label="error",
            color="blue",
        )
        plt.savefig(plot_file_name)
