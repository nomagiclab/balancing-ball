from typing import List

from position_prediction.abc_predicter import ABCPredicter


class NoPredictionPredicter(ABCPredicter):
    def __init__(self):
        self.last_position = None

    def add_position(self, position: List[float]):
        self.last_position = position

    def next_position(self) -> List[float]:
        return self.last_position
