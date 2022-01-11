from utils.derivative_calculator import DerivativeCalculator
from utils.integral_calculator import IntegralCalculator


class SingleVarPIDController:
    def __init__(self, kp: float, ki: float, kd: float, max_output: float, min_output: float):
        assert max_output >= min_output

        self.kp = kp
        self.ki = ki
        self.kd = kd

        self.max_output = max_output
        self.min_output = min_output

        self._derivative_calculator = DerivativeCalculator()
        self._integral_calculator = IntegralCalculator()

    def get_integral(self):
        return self._integral_calculator.get_current_integral()

    def get_derivative(self):
        return self._derivative_calculator.get_current_derivative()

    def compute(self, error: float, time: float):
        error_integral = self._integral_calculator.get_and_update_integral(error, time)
        error_derivative = self._derivative_calculator.get_and_update_derivative(error, time)

        return self._limit_value(self.kp * error + self.ki * error_integral + self.kd * error_derivative)

    def _limit_value(self, value: float) -> float:
        return max(min(value, self.max_output), self.min_output)

    def reset(self):
        self._derivative_calculator = DerivativeCalculator()
        self._integral_calculator = IntegralCalculator()
