"""
    Based on useful examples: https://github.com/IntelRealSense/librealsense/tree/jupyter/notebooks
"""
from typing import Tuple, Optional

import cv2
import numpy as np
import pyrealsense2 as rs
from src.vision.camera import AbstractCameraService
from src.segmentation.segmentation import (
    ORANGE_MIN,
    ORANGE_MAX,
    DEFAULT_BLUR_KERNEL,
    bitmask_average_from_img,
)


class UsbRealsenseCamera(AbstractCameraService):
    @staticmethod
    def intrinsics():
        return np.array(
            [
                [909.4387817382812, 0.0, 632.1474609375],
                [0.0, 907.5307006835938, 347.2157897949219],
                [0.0, 0.0, 1.0],
            ]
        )

    @staticmethod
    def pose():
        cam_pose = np.loadtxt(
            "environments/ur5e/handeye_calibration/results/camera_pose.txt",
            delimiter=" ",
        )
        return cam_pose[0:3, 0:3], cam_pose[0:3, 3]

    @staticmethod
    def shape() -> Tuple[int, int]:
        return 1280, 720

    def __init__(self, center_point=(0, 0), gui=False):
        super().__init__()
        self.pipe = rs.pipeline()
        self.cfg = rs.config()
        self.profile = self.pipe.start(self.cfg)

        self.center_point = center_point

        self.__gui = gui
        self.init_gui()

        # Skip 5 first frames to give the Auto-Exposure time to adjust
        for x in range(5):
            self.pipe.wait_for_frames()

    def init_gui(self):
        if self.__gui:
            self.__gui_window_name = "rgb vision"
            cv2.namedWindow(self.__gui_window_name, cv2.WINDOW_AUTOSIZE)

    def raw_realsense_photo(self):
        # Store next frameset for later processing:
        frameset = self.pipe.wait_for_frames()

        # Create alignment primitive with color as its target stream:
        align = rs.align(rs.stream.color)
        frameset = align.process(frameset)

        # Update color and depth frames:
        color_frame = frameset.get_color_frame()

        aligned_depth_frame = frameset.get_depth_frame()
        return color_frame, aligned_depth_frame

    def raw_photo(self, colorized_depth=False):
        color_frame, aligned_depth_frame = self.raw_realsense_photo()
        color = np.asanyarray(color_frame.get_data())
        if colorized_depth:
            colorizer = rs.colorizer()
            aligned_depth_frame = np.asanyarray(
                colorizer.colorize(aligned_depth_frame).get_data()
            )
        else:
            aligned_depth_frame = np.asanyarray(aligned_depth_frame.get_data())

        depth_scale = self.profile.get_device().first_depth_sensor().get_depth_scale()
        return color, aligned_depth_frame * depth_scale

    def take_photo(self):
        color, depth = self.raw_photo(colorized_depth=False)
        return color, depth, None

    def object_position(self) -> Optional[Tuple[float, float]]:
        rgb, _, _ = self.take_photo()

        position = bitmask_average_from_img(
            rgb,
            blur_kernel=DEFAULT_BLUR_KERNEL,
            COLOR_MIN=ORANGE_MIN,
            COLOR_MAX=ORANGE_MAX,
        )

        if self.__gui:
            image = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)

            if position is not None:
                cv2.circle(
                    image, tuple(int(x) for x in position), 5, (0, 0, 255), cv2.FILLED
                )

            cv2.circle(
                image,
                tuple(int(x) for x in self.center_point),
                5,
                (0, 255, 0),
                cv2.FILLED,
            )
            cv2.imshow(self.__gui_window_name, image)

        if position is None:
            return None

        return position[0] - self.center_point[0], position[1] - self.center_point[1]

    def gui_wait_key(self):
        if self.__gui:
            cv2.waitKey(5)

    def __del__(self):
        self.pipe.stop()
        cv2.destroyAllWindows()
