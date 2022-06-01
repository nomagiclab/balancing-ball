from typing import List

from position_prediction.abc_predicter import ABCPredicter

"""
For details please visit: 
https://www.researchgate.net/publication/334980885_Prediction_of_a_Ball_Trajectory_for_the_Humanoid_Robots_A_Friction-Based_Study
https://en.wikipedia.org/wiki/Exponential_smoothing
"""
class NoPredictionPredicter(ABCPredicter):
    def __init__(self):
        pass

    def add_position(self, position: List[float]):
        self.last_position = position

    def next_position(self) -> List[float]:
        return self.last_position