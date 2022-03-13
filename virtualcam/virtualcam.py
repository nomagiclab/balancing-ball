from typing import List
from utils.button import Button
from math import sqrt
from src.vision.camera import AbstractCameraService
from numpy import asarray, matmul
from numpy.linalg import inv
from PIL import Image


# Class represents a virtual camera.
class VirtualCam(AbstractCameraService):

	# Initialize the virtual camera by pybullet client, 
	# camera position and the shape of photos. 
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


	# Returns the shape of the photo.
	def shape(self):
		return self.width, self.height


	# Takes and returns photos taken by virtual camera.
	def take_photo(self):
		self.last_width, self.last_height, self.rgb_img, self.depth_img, self.seg_img = self.client.getCameraImage(
			width=self.width,
			height=self.height,
			viewMatrix=self.view_matrix,
			projectionMatrix=self.projection_matrix)
		# print(self.search_for_ball())
		# print(self.search_for_paddle())
		im = Image.fromarray(self.rgb_img)
		im.save("image.png")
		return self.rgb_img, self.depth_img, self.seg_img


	# Takes the photo if button is clicked.
	def check_and_take_photo(self):
		if self.take_photo_button.was_clicked():
			self.take_photo()
			self.get_objects_location(take_photo=False)


	# Returns matrix transposing 3d world coordinates with changed origin to 2d picture.
	def intrinsics(self):
		return projection_matrix


	# Returns matrix changing the position and orientation of origin.
	def pose(self):
		return view_matrix


	# Translates pixel from the previous picture into 3d world coordinates.
	# https://stackoverflow.com/questions/59128880/getting-world-coordinates-from-opengl-depth-buffer
	def translate_to_origin_frame(self, w: int, h: int):
		x = (2*w - self.last_width)/self.last_width
		y = -(2*h - self.last_height)/self.last_height
		z = 2*float(self.depth_img[h,w]) - 1

		print("pixel position: ", w, h)
		print("vector position: ", x, y, z)
		pix_pos = asarray([x, y, z, 1])
		position = matmul(self.transform_matrix, pix_pos)
		return position / position[3]


	# Checks whether pixel from the previous picture belongs to the ball.
	def is_ball_pixel(self, h: int, w: int):
		return 	(max(self.rgb_img[h,w][:3]) - min(self.rgb_img[h,w][:3]) < 2 and
				float(self.depth_img[h,w]) < 0.9 and 
				min(self.rgb_img[h,w][:3]) < 225 and 
				min(self.rgb_img[h,w][:3]) > 50)


	# Checks whether pixel from the previous picture belongs to the paddle.
	def is_paddle_pixel(self, h: int, w: int):
		return max(self.rgb_img[h,w][1:3]) == 0 and self.rgb_img[h,w][0] > 10


	# Finds the center of the ball in the previous picture (in terms of the pixels).
	# Returns none if have not found it.
	def search_for_ball(self):
		cnt = 0
		center = [0, 0]
		for h in range(0, self.last_height):
			for w in range(0, self.last_width):
				if self.is_ball_pixel(h, w):
					self.rgb_img[h,w][:3] = [85, 255, 0]
					center[0] += h
					center[1] += w
					cnt += 1
		if cnt == 0:
			return None
		center[0] /= cnt
		center[1] /= cnt
		return center


	# Finds the center of the paddle in the previous picture (in terms of the pixels).
	# Return none if have not found it.
	def search_for_paddle(self):
		cnt = 0
		center = [0, 0]
		for h in range(0, self.last_height):
			for w in range(0, self.last_width):
				if self.is_paddle_pixel(h, w):
					self.rgb_img[h,w][:3] = [0, 68, 255]
					center[0] += h
					center[1] += w
					cnt += 1
		if cnt == 0:
			return None
		center[0] /= cnt
		center[1] /= cnt
		return center


	# Finds the 3d world coordinates of the ball and paddle in the previous picture.
	# If take_photo is set, takes a photo before
	def get_objects_location(self, take_photo=True): 
		if take_photo:
			self.take_photo()
		# print("Searching ball...")
		center_ball = self.search_for_ball()
		# print("Searching paddle...")
		center_paddle = self.search_for_paddle()
		# print("ball: ")
		pos_ball = self.translate_to_origin_frame(int(center_ball[1]), int(center_ball[0]))
		# print("paddle: ")
		pos_paddle = self.translate_to_origin_frame(int(center_paddle[1]), int(center_paddle[0]))
		print("Ball position: ", pos_ball)
		print("Paddle position: ", pos_paddle)
		return center_ball, center_paddle

