from collections import deque
from typing import Tuple, List

from scipy import interpolate
import numpy as np

import time

from position_prediction.abc_predicter import ABCPredicter

"""
For details please visit: 
https://www.researchgate.net/publication/334980885_Prediction_of_a_Ball_Trajectory_for_the_Humanoid_Robots_A_Friction-Based_Study
https://en.wikipedia.org/wiki/Exponential_smoothing
"""
class DESPredicter(ABCPredicter):
    def __init__(self, delay, good_fetch_time, alpha=0.5, gamma=0.001):
        self.alpha = alpha
        self.gamma = gamma
        self.S = [None, None, None]
        self.B = [None, None, None]
        self.delay = delay
        self.good_fetch_time = good_fetch_time
        self.own_timer = time.time()

    def recalculate_S_and_B(self, index, last_pos, a, g):
        if self.S[index] is None:
                self.S[index] = last_pos
        elif self.B[index] is None:
                self.B[index] = last_pos - self.S[index]
        else:
                prev_S = self.S[index]
                prev_B = self.B[index]
                self.S[index] = a*last_pos + (1-a)*(prev_S + prev_B)
                new_S = self.S[index]
                self.B[index] = g*(new_S - prev_S) + (1-g)*prev_B
        

    def add_position(self, position: List[float]):
        for index, pos in enumerate(position):
                self.recalculate_S_and_B(index, pos, 1, self.gamma)
        self.own_timer = time.time()

    def next_position(self) -> List[float]:
        predicted = [self.predict(i) for i in range(3)]
        if time.time() - self.own_timer >= self.good_fetch_time:
                for index, pos in enumerate(predicted):
                        self.recalculate_S_and_B(index, pos, self.alpha, self.gamma)
                self.own_timer = time.time()
        print(self.S, self.B)
        return predicted

    def predict(self, index) -> float:
        last_S = self.S[index]
        last_B = self.B[index]
        if last_S is None:
                raise RuntimeError('Predicting without initial position') from None
        if last_B is None:
                return last_S
        return last_S + self.delay*last_B