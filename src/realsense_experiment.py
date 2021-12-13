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

for i in range(1):
    color, depth = camera.raw_photo()

    frame_threshed = blurred_thresholding(color)
    print("DISTANCE:", calculate_distance(frame_threshed, depth))
    frame_threshed = np.expand_dims(frame_threshed, axis=-1)

    color = convert(color)
    frame_threshed = convert(frame_threshed)

    depth = torch.Tensor(depth)/np.average(depth)

    save_image(color, dir_name +  f'color{i}.png')
    save_image(depth, dir_name +  f'depth{i}.png')
    save_image(frame_threshed, dir_name + f'frame_threshed{i}.png')
    time.sleep(1)
