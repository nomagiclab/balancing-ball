from typing import Union, Tuple

from trackers.ball_tracker import BallTracker, OutOfRange
from pid.pid_controller import PIDController

OUT_OF_RANGE = -1


class PIDBalancer:
    def __init__(
        self, tracker: BallTracker, controller: PIDController, time_step: float = 0.008
    ):
        self.tracker = tracker
        self.controller = controller
        self.time_step = time_step
        self.current_time = 0

    def calculate_next_angle(self) -> Union[Tuple[float, float], int]:
        try:
            err = self.tracker.get_error_vector()
            res = self.controller.compute(err, self.current_time)

            self.current_time += self.time_step

            return res
        except OutOfRange:
            self.controller.reset()
            return OUT_OF_RANGE

    def next_angle_generator(self) -> Union[Tuple[float, float], int]:
        while True:
            yield self.calculate_next_angle()

    def change_pid_coefficients(
        self, kp: float = None, ki: float = None, kd: float = None
    ):
        self.controller.reset_coefficients(kp, ki, kd)
