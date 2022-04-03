from abc import ABC, abstractmethod


class ABCPaddle(ABC):
    @abstractmethod
    def set_angles(self, x_angle: float, y_angle: float):
        """All params should be given in degrees."""
        pass

    @abstractmethod
    def reset_torque_pos(self):
        pass
