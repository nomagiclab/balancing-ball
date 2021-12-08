from typing import Tuple, Optional
import torch
import numpy as np
import abc


""" First 3 coordinates on axis=0 are rgb, last coordinates on this axis is/are depth. """
HeightMapImage = torch.Tensor
CameraPose = Tuple[np.ndarray, np.ndarray]
CameraMatrix = np.ndarray


class AbstractCameraService(abc.ABC):
    RGBImage = np.ndarray
    DepthImage = np.ndarray
    SegmentationImage = np.ndarray
    Photo = Tuple[RGBImage, Optional[DepthImage], Optional[SegmentationImage]]

    @abc.abstractmethod
    def shape(self) -> Tuple[int, int]:
        """ Returns (height, width) of the resulting image. """

    @abc.abstractmethod
    def take_photo(self) -> Photo:
        """ Returns rgb, optionally depth, optionally segmentation. """

    @abc.abstractmethod
    def intrinsics(self):
        """ Returns intrinsics matrix of the camera. """

    @abc.abstractmethod
    def pose(self):
        """ Returns the pose of the camera (3x3-dim rotation matrix, 3-dim translation vector)
            in the robot coordinate system. """
