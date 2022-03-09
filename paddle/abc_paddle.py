from abc import ABC, abstractmethod
from typing import List


class ABCPaddle(ABC):
    @abstractmethod
    def set_angle_on_axis(self, axis: str, angle: float):
        """Parameter `angle` should be given in degrees."""
        pass

    @abstractmethod
    def rotate_around_axis(self, axis: str, angle: float):
        """Parameter `angle` should be given in degrees."""
        pass

    @abstractmethod
    def move_by_vector(self, vector: List[float]):
        """Parameter `vector` is in [x, y, z] order"""
        pass

    @abstractmethod
    def move_to_position(self, position: List[float]):
        """Parameter `position` is in [x, y, z] order"""
        pass

    @abstractmethod
    def get_center_position(self) -> List[float]:
        """Returns [x, y, z] coordinates of the center"""
        pass

    @abstractmethod
    def check_if_in_range(self, position: List[float]) -> bool:
        """Parameter `position` is in [x, y, z] order"""
        pass

    @abstractmethod
    def reset_torque_pos(self):
        pass
