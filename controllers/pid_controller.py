from typing import Tuple, List


class PIDController:
    __debug = False

    def __init__(self, kp: float, ki: float, kd: float, max_output: float, min_output: float):
        assert max_output >= min_output

        self.kp = kp
        self.ki = ki
        self.kd = kd

        self.max_output = max_output
        self.min_output = min_output

        self._last_error = [0, 0]
        self._i_error = [0, 0]
        self._last_time = 0

    def debug_on(self):
        self.__debug = True

    def debug_off(self):
        self.__debug = False

    def compute(self, current_time: float, current_error: List[float]) -> Tuple[float, float]:
        if self._last_time == 0:
            self._last_time = current_time

        dt = current_time - self._last_time

        # Calculate the proportional error.
        p_error = [x for x in current_error]

        # Calculate the integral error.
        for i in range(2):
            self._i_error[i] += current_error[i] * dt

        # TODO - There should be a system that prevents integral windup problem.

        # Calculate the derivative error.
        if dt > 0:
            d_error = [(current_error[i] - self._last_error[i]) / dt for i in range(2)]
        else:
            d_error = [0, 0]

        self._last_error = [x for x in current_error]
        self._last_time = current_time

        if self.__debug:
            print("PID errors (P, I, D):", p_error, self._i_error, d_error)

        # TODO - There should be a system that smooths the paddle swings.
        output = (self._limit_value(self.kp * p_error[0] + self.ki * self._i_error[0] + self.kd * d_error[0]),
                  self._limit_value(self.kp * p_error[1] + self.ki * self._i_error[1] + self.kd * d_error[1]))

        if self.__debug:
            print("PID output:", output)

        return output

    def reset(self):
        if self.__debug:
            print("PID reset!")

        self._last_error = [0, 0]
        self._i_error = [0, 0]
        self._last_time = 0

    def _limit_value(self, value: float) -> float:
        return max(min(value, self.max_output), self.min_output)
