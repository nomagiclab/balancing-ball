from abc import ABC, abstractmethod
from typing import List


class ABCBall(ABC):
    def __init__(self,  *args, **kwargs):
        pass

    @abstractmethod
    def get_position(self) -> List[float]:
        pass
