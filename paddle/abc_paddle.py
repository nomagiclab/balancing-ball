from abc import ABC, abstractmethod, abstractproperty


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
    def move_by_vector(self, v):
        pass

    @abstractmethod
    def move_to_position(self, p):
        pass

    #TODO: Nie wiem czy to w ogóle będzie potrzebne?
    '''
    @abstractmethod
    def create_gui_controlls(self):
        pass
    '''