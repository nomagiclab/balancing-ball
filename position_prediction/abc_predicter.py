from abc import ABC, abstractmethod
from typing import Tuple, List


class ABCPredicter(ABC):
    @abstractmethod
    def add_position(self, position: List[float]):
        pass

    @abstractmethod
    def next_position(self) -> List[float]:
        pass
