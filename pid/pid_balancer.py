import time
from typing import Union, Tuple

from trackers.abstract_tracker import AbstractBallTracker, OutOfRange
from pid.pid_controller import PIDController

OUT_OF_RANGE = (-1, -1)


class PIDBalancer:
    def __init__(
        self,
        tracker: AbstractBallTracker,
        controller: PIDController,
        time_step: float = 0.008,
    ):
        self.tracker = tracker
        self.controller = controller
        self.time_step = time_step
        self.current_time = 0
        self.last_err = 0

    def calculate_next_angle(self, real_time=False) -> Union[Tuple[float, float], int]:
        try:
            err = self.tracker.get_error_vector()

            self.last_err = err

            if real_time:
                self.current_time = time.time()

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
