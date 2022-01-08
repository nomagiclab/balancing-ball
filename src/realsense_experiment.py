import torch
from torchvision.utils import save_image
import cv2 as cv
import time 
import numpy as np

import os

from vision.realsense import UsbRealsenseCamera
from segmentation.segmentation import blurred_thresholding, calculate_distance



dir_name = 'imgs/'

camera = UsbRealsenseCamera()

os.makedirs(dir_name, exist_ok=True)

def convert(t: np.ndarray):
    return torch.Tensor(t).permute(2, 0, 1)/255

while True:
    color, depth = camera.raw_photo()

    frame_threshed = blurred_thresholding(color)
    print("DISTANCE:", calculate_distance(frame_threshed, depth))
