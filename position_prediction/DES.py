from collections import deque
from typing import Tuple, List

from position_prediction.abc_predicter import ABCPredicter

"""
For details please visit: 
https://www.researchgate.net/publication/334980885_Prediction_of_a_Ball_Trajectory_for_the_Humanoid_Robots_A_Friction-Based_Study
https://en.wikipedia.org/wiki/Exponential_smoothing
"""


class DESPredicter(ABCPredicter):
    def __init__(self, step_num, alpha=0.8, gamma=0.4):
        self.alpha = alpha
        self.gamma = gamma
        self.S = [None, None, None]
        self.B = [None, None, None]
        self.step_num = step_num

    def recalculate_S_and_B(self, index, last_pos, a, g):
        if self.S[index] is None:
            self.S[index] = last_pos
        elif self.B[index] is None:
            self.B[index] = last_pos - self.S[index]
        else:
            prev_S = self.S[index]
            prev_B = self.B[index]
            self.S[index] = a * last_pos + (1 - a) * (prev_S + prev_B)
            new_S = self.S[index]
            self.B[index] = g * (new_S - prev_S) + (1 - g) * prev_B

    def add_position(self, position: List[float]):
        for index, pos in enumerate(position):
            self.recalculate_S_and_B(index, pos, self.alpha, self.gamma)

    def next_position(self) -> List[float]:
        predicted = [self.predict(i) for i in range(3)]
        return predicted

    def predict(self, index) -> float:
        last_S = self.S[index]
        last_B = self.B[index]
        if last_S is None:
            raise RuntimeError("Predicting without initial position") from None
        if last_B is None:
            return last_S
        return last_S + self.step_num * last_B
