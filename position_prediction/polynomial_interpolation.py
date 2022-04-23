from collections import deque
from typing import Tuple, List

from scipy import interpolate
import numpy as np

from position_prediction.abc_predicter import ABCPredicter


class PolynomialPredicter(ABCPredicter):
    def __init__(self, n_predict):
        self.confirmed_positions = deque(maxlen=n_predict)

    def add_position(self, position: List[float]):
        self.confirmed_positions.append(position)

    def next_position(self) -> List[float]:
        a = list(zip(*self.confirmed_positions))
        x_positions, y_positions, z_positions = a[0], a[1], a[2]
        return [
            self.predict(list(x_positions)),
            self.predict(list(y_positions)),
            self.predict(list(z_positions)),
        ]

    def predict(self, positions: List[float]) -> float:
        n = len(positions)
        if n == 1:
            return positions[0]

        time_series = np.arange(n)
        f = interpolate.interp1d(time_series, positions, fill_value="extrapolate")
        return f(n)
