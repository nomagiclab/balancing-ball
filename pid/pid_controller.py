import csv
import pathlib
import time
from typing import Tuple, List

from pid.single_variable_pid import SingleVarPIDController
from plotting.csv_writer import CsvWriter


class PIDController:
    debug = True

    def __init__(
            self, kp: float, ki: float, kd: float, max_output: float, min_output: float
    ):
        self.x_controller = SingleVarPIDController(kp, ki, kd, max_output, min_output)
        self.y_controller = SingleVarPIDController(kp, ki, kd, max_output, min_output)

        if self.debug:
            self.file_name = (
                    "/home/nomagiclab/balancing-ball/plotting/data/pid.csv"
            )
            self.start_time = time.time()

            with open(self.file_name, "a") as f:
                fw = csv.writer(f)
                fw.writerow(["Time", "P_x", "I_x", "D_x", "P_y", "I_y", "D_y"])

    def compute(
            self, current_error: List[float], current_time: float
    ) -> Tuple[float, float]:
        # TODO - There should be a system that prevents integral windup problem.
        output_x = self.x_controller.compute(current_error[0], current_time)
        output_y = self.y_controller.compute(current_error[1], current_time)

        if self.debug:
            with open(self.file_name, "a") as f:
                fw = csv.writer(f)
                fw.writerow([1000 * (time.time() - self.start_time),
                             self.x_controller.p_error,
                             self.x_controller.get_integral(),
                             self.x_controller.get_derivative(),
                             self.y_controller.p_error,
                             self.y_controller.get_integral(),
                             self.y_controller.get_derivative()])
            print(
                "PID errors (P, I, D):",
                current_error,
                [
                    self.x_controller.get_derivative(),
                    self.y_controller.get_derivative(),
                ],
                [self.x_controller.get_integral(), self.y_controller.get_integral()],
            )

        # TODO - There should be a system that smooths the paddle swings.
        output = output_x, output_y

        if self.debug:
            print("PID output:", output)

        return output

    def reset(self):
        if self.debug:
            print("PID reset!")

        self.x_controller.reset()
        self.y_controller.reset()

    def reset_coefficients(self, kp: float = None, ki: float = None, kd: float = None):
        if kp is not None:
            self.x_controller.kp = kp
            self.y_controller.kp = kp
        if ki is not None:
            self.x_controller.ki = ki
            self.y_controller.ki = ki
        if kd is not None:
            self.x_controller.kd = kd
            self.y_controller.kd = kd
