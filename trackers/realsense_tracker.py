import timeit
from typing import Tuple, List
from src.vision.realsense import UsbRealsenseCamera
from trackers.abstract_tracker import AbstractBallTracker, OutOfRange


class RealsenseTracker(AbstractBallTracker):
    def __init__(self, center_point: Tuple[float, float], gui: bool = False):
        self.camera = UsbRealsenseCamera(center_point, gui)

    def get_error_vector(self, return_on_lost: List[float] = None) -> List[float]:
        res = self.camera.object_position()

        if res is None:
            if return_on_lost is None:
                raise OutOfRange

            return return_on_lost
        V = [x / y for x,y in zip(res, [0.085, 0.07])]

        return V
