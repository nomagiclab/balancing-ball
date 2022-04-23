import time
from typing import List, Tuple

import numpy as np
import pybullet as p
import math

from ball.pybullet_ball import PyBulletBall
from paddle.abc_paddle import ABCPaddle
from position_prediction.abc_predicter import ABCPredicter


def calculate_rotation(x_angle, y_angle):
    """Returns last column of the rotation projected on the horizontal plane"""
    sin_y = math.sin(y_angle)
    cos_y = math.cos(y_angle)

    sin_x = math.sin(x_angle)
    cos_x = math.cos(x_angle)

    gravity_decomposition = np.array([sin_y, -sin_x * cos_x, cos_y * cos_x])
    return np.array(
        [gravity_decomposition[0] * cos_x, gravity_decomposition[1] * cos_y]
    )


class PhysicalPredictier(ABCPredicter):
    G = 9.81

    M = 0.0027

    def __init__(self, ball: PyBulletBall, paddle: ABCPaddle):
        self.ball = ball
        self.paddle = paddle

        # For now, we use only x and y velocity as
        # we map velocities to horizontal space :(
        self.curr_velocity = np.array([0, 0])
        self.current_position = np.array([0, 0])
        self.last_update = time.time()

        self.last_certain_position = [0, 0, 0]
        self.certain_position_update_time = time.time()

        # Parameter for the running average.
        self.ALPHA = 0.2

    def next_position(self) -> List[float]:
        time_delta = time.time() - self.last_update
        self.last_update = time.time()

        last_velocity = self.curr_velocity

        new_velocity = self.new_velocity(self.curr_velocity, time_delta)
        self.curr_velocity = (
            self.curr_velocity * self.ALPHA + (1 - self.ALPHA) * new_velocity
        )

        self.current_position = (
            self.current_position
            + time_delta * (self.curr_velocity + last_velocity) / 2
        )
        return list(self.current_position)

    def add_position(self, position: List[float]):
        time_delta = time.time() - self.certain_position_update_time
        self.last_update = time.time()
        self.certain_position_update_time = time.time()

        self.curr_velocity = (
            abs((np.array(position[:2]) - self.last_certain_position)) / time_delta
        )
        self.last_certain_position = np.array(position[:2])

    def calculate_acceleration(self) -> np.array:
        """Calculates acceleration projected on horizontal plane"""
        angles = self.paddle.get_angles()
        rotation = self.G * calculate_rotation(angles[0], angles[1])
        return rotation / self.M

    def new_velocity(self, velocity: np.array, time_delta: float) -> np.array:
        return velocity + self.calculate_acceleration() * time_delta
