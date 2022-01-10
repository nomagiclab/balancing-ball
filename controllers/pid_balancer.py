from typing import Union, Tuple

from trackers.ball_tracker import BallTracker, OutOfRange
from controllers.pid_controller import PIDController
from utils.derivative_calculator import DerivativeCalculator

OUT_OF_RANGE = -1


class PIDBalancer:
    def __init__(self, tracker: BallTracker, controller: PIDController, time_step: float = 0.008):
        self.tracker = tracker
        self.controller = controller
        self.time_step = time_step
        self.current_time = 0

        self.x_derivative_calc = DerivativeCalculator(tracker.get_ball_position()[0])
        self.y_derivative_calc = DerivativeCalculator(tracker.get_ball_position()[1])

        self.controller.set_up_derivative_calc(lambda: [self.x_derivative_calc.get_current_derivative(),
                                                        self.y_derivative_calc.get_current_derivative()])

    def _update_derivatives(self) -> None:
        ball_pos = self.tracker.get_ball_position()

        self.x_derivative_calc.update_derivative(ball_pos[0])
        self.y_derivative_calc.update_derivative(ball_pos[1])

    def calculate_next_angle(self) -> Union[Tuple[float, float], int]:
        try:
            err = self.tracker.get_error_vector()
            self._update_derivatives()
            res = self.controller.compute(self.current_time, err)

            self.current_time += self.time_step

            return res
        except OutOfRange:
            self.controller.reset()
            return OUT_OF_RANGE

    def next_angle_generator(self) -> Union[Tuple[float, float], int]:
        while True:
            yield self.calculate_next_angle()

    def change_pid_coefficients(self, p: float = None, i: float = None, d: float = None):
        if p is not None:
            self.controller.kp = p
        if i is not None:
            self.controller.ki = i
        if d is not None:
            self.controller.kd = d
