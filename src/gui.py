import torch
from torchvision.utils import save_image
import cv2 as cv
import time 
import numpy as np

import os

from vision.realsense import UsbRealsenseCamera
from segmentation.segmentation import blurred_thresholding

camera = UsbRealsenseCamera()

while True:
	#img = cv.imread('imgs/color0.png')
	rgb, _, _ = camera.take_photo()
	frame_thresholded = blurred_thresholding(rgb)
	height, width = camera.shape()
	xs, ys = np.meshgrid(np.linspace(0, height-1, height), np.linspace(0, width-1, width))
	suma = np.sum(frame_thresholded)
	rgb = cv.cvtColor(rgb, cv.COLOR_RGB2BGR)
	if suma != 0:
		xs = xs * frame_thresholded
		ys = ys * frame_thresholded
		avg_x = int(np.sum(xs)/suma)
		avg_y = int(np.sum(ys)/suma)
		print(avg_x, avg_y)
		frame_thresholded = np.dstack((frame_thresholded, frame_thresholded, frame_thresholded))
		frame_thresholded = cv.circle(frame_thresholded, (avg_x, avg_y), 5, (0,0,255), -1)
	cv.imshow('rgb vision', rgb)
	cv.imshow('th vision', frame_thresholded)
	
	cv.waitKey(5) # waits until a key is pressed