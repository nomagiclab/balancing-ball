from typing import Tuple, List

from scipy import interpolate
import numpy as np

from position_prediction.abc_predicter import ABCPredicter


class PolynomialPredicter(ABCPredicter):
    def predict(self, positions: List[float], position_index: int) -> float:
        n = len(positions)
        if n == 1:
            return positions[0]

        time_series = np.arange(n)
        f = interpolate.interp1d(time_series, positions, fill_value="extrapolate")
        return f(n + position_index)

    def predict_x_y(
        self, positions: List[Tuple[float, float, float]], position_index: int
    ) -> Tuple[float, float, float]:
        a = list(zip(*positions))
        x_positions, y_positions, z_positions = a[0], a[1], a[2]
        return (
            self.predict(x_positions, position_index),
            self.predict(y_positions, position_index),
            self.predict(z_positions, position_index),
        )
