import torch
from torchvision.utils import save_image
import cv2 as cv
import numpy as np

import os

from vision.realsense import UsbRealsenseCamera
from segmentation.segmentation import blurred_thresholding, bitmask_average

camera = UsbRealsenseCamera()

while True:
    rgb, _, _ = camera.take_photo()
    frame_thresholded = blurred_thresholding(rgb)
    rgb = cv.cvtColor(rgb, cv.COLOR_RGB2BGR)
    bit_average = bitmask_average(frame_thresholded)
    frame_thresholded = np.dstack(
        (frame_thresholded, frame_thresholded, frame_thresholded)
    )
    if bit_average is not None:
        avg_x, avg_y = bit_average
        circle_centre = int(avg_x), int(avg_y)
        frame_thresholded = cv.circle(
            frame_thresholded, circle_centre, 5, (0, 0, 255), -1
        )
    cv.imshow("rgb vision", rgb)
    cv.imshow("th vision", frame_thresholded)

    cv.waitKey(5)  # waits until a key is pressed
