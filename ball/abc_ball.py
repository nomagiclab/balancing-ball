from abc import ABC, abstractmethod
from typing import List

BALL_RADIUS = 0.2


class ABCBall(ABC):
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_position(self) -> List[float]:
        pass
