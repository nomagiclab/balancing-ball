import cv2 as cv
import numpy as np
from typing import Tuple, Optional


BLUE_MIN = np.array([100, 40, 40],np.uint8)
BLUE_MAX = np.array([140, 255, 255],np.uint8)

ORANGE_MIN = np.array([6, 80, 130],np.uint8)
ORANGE_MAX = np.array([15, 255, 255],np.uint8)

DEFAULT_BLUR_KERNEL = (10, 10)

"""
Returns result of raw_thesholding on blurred image.

Image has to be of RBG type with integer values in range [0, 255].
"""
def blurred_thresholding(img: np.ndarray,
			 blur_kernel: Tuple[int, int] = DEFAULT_BLUR_KERNEL,
			 COLOR_MIN: np.ndarray = ORANGE_MIN,
			 COLOR_MAX: np.ndarray = ORANGE_MAX) -> np.ndarray:
	blurred_img = cv.blur(img, blur_kernel)
	return raw_thesholding(blurred_img, COLOR_MIN=COLOR_MIN, COLOR_MAX=COLOR_MAX)

"""
Returns result of color thersholding on img.
Value in the array is 255 if color is detected, 0 otherwise.

Image has to be of RBG type with integer values in range [0, 255].
"""
def raw_thesholding(img: np.ndarray,
		    COLOR_MIN: np.ndarray = ORANGE_MIN, 
		    COLOR_MAX: np.ndarray = ORANGE_MAX) -> np.ndarray:
	hsv = cv.cvtColor(img, cv.COLOR_RGB2HSV)
	return cv.inRange(hsv, COLOR_MIN, COLOR_MAX)
"""
Returns average of x and y coordinates of turned on bits in bitmask.

None if there aren't any lit up bits.
"""
def bitmask_average(bitmask: np.ndarray) -> Optional[Tuple[float, float]]:
	total_bits = np.sum(bitmask)
	if total_bits == 0:
		return None
	
	height, width = bitmask.shape
	xs, ys = np.meshgrid(np.linspace(0, width-1, width), np.linspace(0, height-1, height))
	turned_on_xs = xs * bitmask
	turned_on_ys = ys * bitmask
	avg_x = np.sum(turned_on_xs)/total_bits
	avg_y = np.sum(turned_on_ys)/total_bits
	return avg_x, avg_y



def calculate_distance(mask: np.ndarray,
		       depth: np.ndarray) -> float:
	mask_pixels = np.sum(mask > 0)
	#TODO: define this behaviour
	if mask_pixels == 0:
		return -1
	return np.sum(depth * (mask > 0))/mask_pixels