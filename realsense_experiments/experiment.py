from realsense import UsbRealsenseCamera
import torch
from torchvision.utils import save_image
import cv2 as cv
import time 
import numpy as np

dir_name = 'imgs/'

COLOR_MIN = np.array([100, 40, 0],np.uint8)
COLOR_MAX = np.array([140, 200, 200],np.uint8)

camera = UsbRealsenseCamera()

def convert(t: np.ndarray):
    return torch.Tensor(t).permute(2, 0, 1)/255

for i in range(1):
    color, depth = camera.raw_photo(colorized_depth = True)

    blurred = cv.blur(color, (10, 10))
    
    hsv = cv.cvtColor(blurred, cv.COLOR_RGB2HSV)
    frame_threshed = cv.inRange(hsv, COLOR_MIN, COLOR_MAX)
    frame_threshed = np.expand_dims(frame_threshed, axis=-1)
    print(frame_threshed.shape)
    print(blurred.shape)

    color = convert(color)
    blurred = convert(blurred)
    frame_threshed = convert(frame_threshed)

    depth = torch.Tensor(depth).permute(2, 0, 1)

    save_image(color, dir_name +  f'color{i}.png')
    save_image(blurred, dir_name + f'blurred{i}.png')
    save_image(depth, dir_name +  f'depth{i}.png')
    save_image(frame_threshed, dir_name + f'frame_threshed{i}.png')
    time.sleep(1)
