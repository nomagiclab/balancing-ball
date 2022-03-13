import torch
from torchvision.utils import save_image
import cv2 as cv
import time
import numpy as np

import os

from vision.realsense import UsbRealsenseCamera
from segmentation.segmentation import blurred_thresholding


dir_name = "imgs/"

camera = UsbRealsenseCamera()

os.makedirs(dir_name, exist_ok=True)


def convert(t: np.ndarray):
    return torch.Tensor(t).permute(2, 0, 1) / 255


for i in range(1):
    color, depth = camera.raw_photo(colorized_depth=True)

    frame_threshed = blurred_thresholding(color)
    frame_threshed = np.expand_dims(frame_threshed, axis=-1)

    color = convert(color)
    frame_threshed = convert(frame_threshed)

    depth = torch.Tensor(depth).permute(2, 0, 1)

    save_image(color, dir_name + f"color{i}.png")
    save_image(depth, dir_name + f"depth{i}.png")
    save_image(frame_threshed, dir_name + f"frame_threshed{i}.png")
    time.sleep(1)
