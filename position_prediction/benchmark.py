import csv
import time
from datetime import date

import pandas
import pybullet

from paddle.abc_paddle import ABCPaddle
from trackers.abstract_tracker import AbstractBallTracker
from ball.pybullet_ball import PyBulletBall
from utils.environment import set_wind
from utils.pid_performer import PidPerformer


class Benchmark:
    TESTS_WIND = [(-1.5, 0.0), (1.5, 0.0), (0.0, 1.5), (0.0, -1.5), (0.9, 0.9), (-0.9, 0.9), (-0.9, -0.9), (0.9, -0.9)]

    def __init__(self, tracker: AbstractBallTracker, ball: PyBulletBall, csv_file_name: str = None):
        assert hasattr(tracker, 'last_predicted_pos')

        self.tracker = tracker
        self.ball = ball

        if csv_file_name is None:
            csv_file_name = "benchmark" + date.today().strftime("%b-%d-%Y") + ".csv"

        self.csv_file_name = csv_file_name
        self.csv_file = open(self.csv_file_name, "w")
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(["Frame", "X", "Y", "Z", "X_pred", "Y_pred", "Z_pred"])

    def run_benchmark(self, pybullet_client: pybullet, paddle: ABCPaddle):
        pid_performer = PidPerformer(pybullet_client, self.tracker, paddle)

        average_error = (0, 0, 0)

        frame = 0
        predicted_frames = 0

        test = -1
        time_left = 5.0
        last_time = time.time()

        while True:
            if time_left <= 0.0:
                test += 1

                if test >= len(self.TESTS_WIND):
                    print("Benchmark finished!")
                    print("Average error (x, y, z): " + str(tuple(average_error[i] / frame for i in range(3))))
                    break

                set_wind(pybullet_client, *self.TESTS_WIND[test])
                time_left = 1.0

            paddle.read_and_update_joint_position()

            pid_performer.perform_pid_step()

            predicted_pos = self.tracker.last_predicted_pos

            if predicted_pos is not None:
                real_pos = self.ball.get_position()

                self.csv_writer.writerow([frame, *real_pos, *predicted_pos])

                average_error = tuple(average_error[i] + abs(predicted_pos[i] - real_pos[i]) for i in range(3))
                predicted_frames += 1

            frame += 1

            time_left -= (time.time() - last_time)
            last_time = time.time()

            pybullet_client.stepSimulation()
            time.sleep(0.01)

        self.csv_file.close()

    @staticmethod
    def plot_linear(csv_file_name: str):
        from matplotlib import pyplot as plt

        data = pandas.read_csv(csv_file_name)
        plt.plot(data["Frame"], abs(data["X_pred"] - data["X"]), label="X", color="red")
        plt.plot(data["Frame"], abs(data["Y_pred"] - data["Y"]), label="Y", color="green")
        #plt.plot(data["Frame"], abs(data["Z_pred"] - data["Z"]), label="Z", color="blue")
        plt.show()
