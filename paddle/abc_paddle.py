from abc import ABC, abstractmethod
from typing import List


class ABCPaddle(ABC):
    @abstractmethod
    def set_angles(self, x_angle: float, y_angle: float):
        """All params should be given in degrees."""
        pass

    @abstractmethod
    def get_angles(self) -> List[float]:
        """Returns xyz paddle angles in radians."""
        pass

    @abstractmethod
    def reset_torque_pos(self):
        pass
