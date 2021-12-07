from abc import ABC, abstractmethod
from typing import List


class ABCPaddle(ABC):
    @property
    @abstractmethod
    def urdf_model(self):
        pass

    def __init__(self, pybullet_client, *args, **kwargs):
        self.pybullet_client = pybullet_client

        self.robot_id = self.pybullet_client.loadURDF(self.urdf_model, *args, **kwargs)

    @abstractmethod
    def rotate_around_axis(self, axis, angle):
        pass

    @abstractmethod
    def move_by_vector(self, vector: List[float]):
        pass

    @abstractmethod
    def move_to_position(self, position: List[float]):
        pass

    @abstractmethod
    def get_center_position(self) -> List[float]:
        pass

    def check_if_in_range(self, position: List[float]) -> bool:
        pass

    #TODO: Will this be even useful someday?
    '''
    @abstractmethod
    def create_gui_controlls(self):
        pass
    '''