from typing import List
from utils.button import Button
from math import sqrt
from src.vision.camera import AbstractCameraService


# class VirtualCam:
# 	def __init__(self, p, pos: List[float]):
# 		dist = sqrt(pos[0] ** 2 + pos[1] ** 2)
# 		self.client = p
# 		self.view_matrix = p.computeViewMatrix(
# 			cameraEyePosition=pos,
# 			cameraTargetPosition=[0, 0, 0.5],
# 			cameraUpVector=[pos[0], pos[1], pos[2] + 1])
# 		self.projection_matrix = p.computeProjectionMatrixFOV(
# 			fov=45.0,
# 			aspect=1.0,
# 			nearVal=max(0, dist - 1),
# 			farVal=dist + 1)
# 		self.take_photo_button = Button(
# 			p.addUserDebugParameter("Take a photo", 1, 0, 0))
# 		self.width = 240
# 		self.height = 240


# 	def check_and_take_photo(self):
# 		if self.take_photo_button.was_clicked():
# 			self.client.getCameraImage(
# 				width=self.width,
# 				height=self.height,
# 				viewMatrix=self.view_matrix,
# 				projectionMatrix=self.projection_matrix)


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
			farVal=dist + 1)
		self.take_photo_button = Button(
			p.addUserDebugParameter("Take a photo", 1, 0, 0))
		self.width = 240
		self.height = 240


	def shape(self):
		return self.width, self.height


	def take_photo(self):
		width, height, rgbImg, depthImg, segImg = self.client.getCameraImage(
			width=self.width,
			height=self.height,
			viewMatrix=self.view_matrix,
			projectionMatrix=self.projection_matrix)
		return rgbImg, depthImg, segImg


	def check_and_take_photo(self):
		if self.take_photo_button.was_clicked():
			self.take_photo()


	def intrinsics(self):
		return None


	def pose(self):
		return None
