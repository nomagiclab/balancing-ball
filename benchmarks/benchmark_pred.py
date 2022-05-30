import csv
import time
from datetime import date

import pandas
import pybullet

from ball.pybullet_ball import PyBulletBall
from paddle.paddle import Paddle
from trackers.abstract_tracker import AbstractBallTracker
from utils.environment import set_wind
from utils.pid_performer import PidPerformer
import matplotlib as plt
from typing import List


class Benchmark:
    # Time it takes for ball to stabilize.
    INITIAL_WAIT_TIME = 5.0

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
    ):
        if TESTS_WIND is None:
            TESTS_WIND = self.DEFAULT_TESTS_WIND

        assert hasattr(tracker, "last_predicted_pos")

        self.tracker = tracker
        self.ball = ball
        self.TESTS_WIND = TESTS_WIND

        # if csv_file_name is None:
        #     csv_file_name = "benchmark" + date.today().strftime("%b-%d-%Y") + ".csv"
        #
        # self.csv_file_name = csv_file_name
        # self.csv_file = open(self.csv_file_name, "w")
        # self.csv_writer = csv.writer(self.csv_file)
        # self.csv_writer.writerow(["Frame", "X", "Y", "Z", "X_pred", "Y_pred", "Z_pred"])

    def run_benchmark(
        self, pybullet_client: pybullet, paddle: Paddle, wind_period_length=5.0
    ):
        pid_performer = PidPerformer(pybullet_client, self.tracker, paddle)

        average_error = (0, 0, 0)

        frame = 0
        predicted_frames = 0

        test = -1
        time_left = self.INITIAL_WAIT_TIME
        last_time = time.time()

        PYBULLET_TIME_STEP = 1 / 240

        while True:
            start_time = time.time()
            if not paddle.check_if_in_range(self.ball.get_position()):
                print("Benchmark failed, ball out of range!")
                print(
                    "Average error (x, y, z): "
                    + str(tuple(average_error[i] / frame for i in range(3)))
                )
                break

            if time_left <= 0.0:
                test += 1

                if test >= len(self.TESTS_WIND):
                    print("Benchmark finished!")
                    print(
                        "Average error (x, y, z): "
                        + str(tuple(average_error[i] / frame for i in range(3)))
                    )
                    break

                set_wind(pybullet_client, *self.TESTS_WIND[test])
                time_left = wind_period_length

            paddle.read_and_update_joint_position()

            pid_performer.perform_pid_step()

            predicted_pos = self.tracker.last_predicted_pos

            if predicted_pos is not None:
                real_pos = self.ball.get_position()

                self.csv_writer.writerow([frame, *real_pos, *predicted_pos])

                average_error = tuple(
                    average_error[i] + abs(predicted_pos[i] - real_pos[i])
                    for i in range(3)
                )
                predicted_frames += 1

            frame += 1

            time_left -= time.time() - last_time
            last_time = time.time()

            pybullet_client.stepSimulation()
            time.sleep(PYBULLET_TIME_STEP - (time.time() - start_time))

        self.csv_file.close()

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
