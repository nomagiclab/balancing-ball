from typing import Tuple, List
from src.vision.realsense import UsbRealsenseCamera
from trackers.abstract_tracker import AbstractBallTracker, OutOfRange


class RealsenseTracker(AbstractBallTracker):
    def __init__(self, center_point: Tuple[float, float], gui: bool = False):
        self.camera = UsbRealsenseCamera(center_point, gui)

    def get_error_vector(self) -> List[float]:
        res = self.camera.object_position()

        if res is None:
            raise OutOfRange

        return [x for x in self.camera.object_position()]
