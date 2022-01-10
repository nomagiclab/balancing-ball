from typing import List
from utils.button import Button
from math import sqrt
from src.vision.camera import AbstractCameraService
from numpy import asarray, matmul
from numpy.linalg import inv
from PIL import Image

class VirtualCam(AbstractCameraService):
	def __init__(self, p, pos: List[float], width: int, height: int):
		super().__init__()
		dist = sqrt(pos[0] ** 2 + pos[1] ** 2)
		self.client = p
		self.view_matrix = p.computeViewMatrix(
			cameraEyePosition=pos,
			cameraTargetPosition=[0, 0, 0.5],
			cameraUpVector=[pos[0], pos[1], pos[2] + 1])
		self.projection_matrix = p.computeProjectionMatrixFOV(
			fov=45.0,
			aspect=1.0,
			nearVal=max(0, dist - 1),
			farVal=dist+3)
		self.near = max(0, dist - 1)
		self.far = dist + 3
		self.take_photo_button = Button(
			p.addUserDebugParameter("Take a photo", 1, 0, 0))
		self.width = 240
		self.height = 240
		projection_matrix = asarray(self.projection_matrix).reshape([4,4],order='F')
		view_matrix = asarray(self.view_matrix).reshape([4,4],order='F')
		self.transform_matrix = inv(matmul(projection_matrix, view_matrix))


	def shape(self):
		return self.width, self.height


	def take_photo(self):
		self.last_width, self.last_height, self.rgb_img, self.depth_img, self.seg_img = self.client.getCameraImage(
			width=self.width,
			height=self.height,
			viewMatrix=self.view_matrix,
			projectionMatrix=self.projection_matrix)
		print(self.search_for_ball())
		print(self.search_for_paddle())
		im = Image.fromarray(self.rgb_img)
		im.save("image.png")
		return self.rgb_img, self.depth_img, self.seg_img


	def check_and_take_photo(self):
		if self.take_photo_button.was_clicked():
			self.take_photo()


	def intrinsics(self):
		return None


	def pose(self):
		return None


	def get_depth(self, w: int, h: int):
		return 2*self.depth_img[h,w] - 1


	def translate_to_origin_frame(self, w: int, h: int):
		x = (2*w - self.last_width)/self.last_width
		y = -(2*h - self.last_height)/self.last_height
		z = 2*float(self.depth_img[h,w]) - 1
		pix_pos = asarray([x, y, z, 1])
		position = matmul(self.transform_matrix, pix_pos)
		return position / position[3]


	def search_for_ball(self):
		avg = 0
		cnt = 0
		center = [0, 0]
		for h in range(0, self.last_height):
			for w in range(0, self.last_width):
				if max(self.rgb_img[h,w][:3]) - min(self.rgb_img[h,w][:3]) < 2 and float(self.depth_img[h,w]) < 0.9 and min(self.rgb_img[h,w][:3]) < 225 and min(self.rgb_img[h,w][:3]) > 50:
					self.rgb_img[h,w][:3] = [85, 255, 0]
					center[0] += h
					center[1] += w
					real_depth = self.far * self.near / (self.far - (self.far - self.near) * self.depth_img[h,w])
					avg += real_depth
					cnt += 1
		avg /= cnt
		center[0] /= cnt
		center[1] /= cnt
		print("Average depth: ", avg)
		print("Center: ", center)
		return avg, center


	def search_for_paddle(self):
		avg = 0
		cnt = 0
		center = [0, 0]
		for h in range(0, self.last_height):
			for w in range(0, self.last_width):
				if max(self.rgb_img[h,w][1:3]) == 0 and self.rgb_img[h,w][0] > 10:
					self.rgb_img[h,w][:3] = [0, 68, 255]
					center[0] += h
					center[1] += w
					real_depth = self.far * self.near / (self.far - (self.far - self.near) * self.depth_img[h,w])
					avg += real_depth
					cnt += 1
		avg /= cnt
		center[0] /= cnt
		center[1] /= cnt
		print("Average depth: ", avg)
		print("Center: ", center)
		return avg, center

