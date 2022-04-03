from typing import Tuple, List

from scipy import interpolate
import numpy as np


class PolynomialPredicter:
    def predict(self, positions: List[float]) -> float:
        n = len(positions)
        if n == 1:
            return positions[0]

        time_series = np.arange(n)
        f = interpolate.interp1d(time_series, positions, fill_value="extrapolate")
        return f(n)

    def predict_x_y(
        self, positions: List[Tuple[float, float, float]]
    ) -> Tuple[float, float, float]:
        a = list(zip(*positions))
        x_positions, y_positions, z_positions = a[0], a[1], a[2]
        return (
            self.predict(x_positions),
            self.predict(y_positions),
            self.predict(z_positions),
        )
