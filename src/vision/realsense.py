"""
    Based on useful examples: https://github.com/IntelRealSense/librealsense/tree/jupyter/notebooks
"""
from typing import Tuple

import numpy as np
import pyrealsense2 as rs
from vision.camera import AbstractCameraService


class UsbRealsenseCamera(AbstractCameraService):
    def __init__(self):
        super().__init__()
        self.pipe = rs.pipeline()
        self.cfg = rs.config()
        self.profile = self.pipe.start(self.cfg)

        # Skip 5 first frames to give the Auto-Exposure time to adjust
        for x in range(5):
            self.pipe.wait_for_frames()

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

    def intrinsics(self):
        return np.array(
            [
                [909.4387817382812, 0.0, 632.1474609375],
                [0.0, 907.5307006835938, 347.2157897949219],
                [0.0, 0.0, 1.0],
            ]
        )

    def pose(self):
        cam_pose = np.loadtxt(
            "environments/ur5e/handeye_calibration/results/camera_pose.txt",
            delimiter=" ",
        )
        return cam_pose[0:3, 0:3], cam_pose[0:3, 3]

    def shape(self) -> Tuple[int, int]:
        return 1280, 720

    def take_photo(self):
        color, depth = self.raw_photo(colorized_depth=False)
        return color, depth, None

    def __del__(self):
        self.pipe.stop()
