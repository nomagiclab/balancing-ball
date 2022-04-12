from abc import ABC, abstractmethod
from typing import Tuple, List


class ABCPredicter(ABC):
    @abstractmethod
    def predict_x_y(
        self, positions: List[Tuple[float, float, float]], position_index: int
    ) -> Tuple[float, float, float]:
        pass
