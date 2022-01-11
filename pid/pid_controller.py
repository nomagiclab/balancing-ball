from typing import Tuple, List

from pid.single_variable_pid import SingleVarPIDController


class PIDController:
    __debug = False

    def __init__(self,
                 kp: float, ki: float, kd: float,
                 max_output: float, min_output: float):
        self.x_controller = SingleVarPIDController(kp, ki, kd, max_output, min_output)
        self.y_controller = SingleVarPIDController(kp, ki, kd, max_output, min_output)

    def compute(self, current_error: List[float], current_time: float) -> Tuple[float, float]:
        # TODO - There should be a system that prevents integral windup problem.
        output_x = self.x_controller.compute(current_error[0], current_time)
        output_y = self.y_controller.compute(current_error[1], current_time)

        if self.__debug:
            print("PID errors (P, I, D):", current_error,
                  [self.x_controller.get_derivative(), self.y_controller.get_derivative()],
                  [self.x_controller.get_integral(), self.y_controller.get_integral()])

        # TODO - There should be a system that smooths the paddle swings.
        output = output_x, output_y

        if self.__debug:
            print("PID output:", output)

        return output

    def reset(self):
        if self.__debug:
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

    def debug_on(self):
        self.__debug = True

    def debug_off(self):
        self.__debug = False
