from abc import ABC, abstractmethod, abstractproperty


class ABCBall(ABC):
    def __init__(self,  *args, **kwargs):
        pass

    @abstractmethod
    def get_position(self):
        pass
