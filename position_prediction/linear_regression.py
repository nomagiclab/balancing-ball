from collections import deque
from turtle import pos
from typing import Tuple, List

from scipy import stats
import numpy as np

from position_prediction.abc_predicter import ABCPredicter


class LinearRegressionPredicter(ABCPredicter):
    def __init__(self, n_predict):
        self.confirmed_positions = deque(maxlen=n_predict)

    def add_position(self, position: List[float]):
        self.confirmed_positions.append(position)

    def next_position(self) -> List[float]:
        a = list(zip(*self.confirmed_positions))
        x_positions, y_positions, z_positions = a[0], a[1], a[2]
        # print("ZWRACAM", self.predict(list(x_positions)))
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
        res = stats.linregress(time_series, positions)
        return res.slope * n + res.intercept
