from abc import ABC, abstractmethod
from typing import List


class AbstractBallTracker(ABC):
    @abstractmethod
    def get_error_vector(self) -> List[float]:
        pass


class OutOfRange(Exception):
    pass
