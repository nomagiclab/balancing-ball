import math
import time
from typing import List

import matplotlib.pyplot as plt
import numpy as np

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


class PlotMaker:
    def __init__(self, labels: List[str]):
        self.data = {label: ([], []) for label in labels}

    def add(self, label, x, y):
        self.data[label][0].append(x)
        self.data[label][1].append(y)

    def __plot(self, p, labels):
        for label in labels:
            p.plot(self.data[label][0], self.data[label][1], label=label)

    def plot(self):
        self.__plot(plt, self.data.keys())
        plt.legend()
        plt.show()

    def plot_subplots(self, subplots: int, labels: List[List[str]]):
        fig, axs = plt.subplots(subplots)
        for i in range(subplots):
            self.__plot(axs[i], labels[i])
        plt.show()


class PhysicalPredictier(ABCPredicter):
    G = 9.81

    M = 0.0027

    def __init__(self, ball: PyBulletBall, paddle: ABCPaddle):
        self.ball = ball
        self.paddle = paddle

        self.debug_plotter = PlotMaker(["real_vel_x", "vel_x", "real_vel_y", "vel_y"])

        # For now, we use only x and y velocity as
        # we map velocities to horizontal space :(
        self.curr_velocity = np.array([0, 0])
        self.current_position = np.array([0, 0])
        self.last_update = time.time()

        self.last_certain_position = [0, 0]
        self.certain_position_update_time = time.time()

        # Parameter for the running average.
        self.ALPHA = 0.2

    def next_position(self) -> List[float]:
        time_delta = time.time() - self.last_update
        print("time_delta next_position", time_delta)
        self.last_update = time.time()

        last_velocity = self.curr_velocity

        new_velocity = self.new_velocity(self.curr_velocity, time_delta)
        print("The new velocity = ", new_velocity)
        self.debug_set_current_velocity(
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

        self.debug_set_current_velocity(
            (np.array(position[:2]) - self.last_certain_position) / time_delta
        )
        print("time_delta", time_delta)
        print(np.array(position[:2]) - self.last_certain_position)
        print("Current velocity", self.curr_velocity)
        self.last_certain_position = np.array(position[:2])

    def debug_set_current_velocity(self, velocity):
        real_vel = self.ball.get_velocity()
        print("Real velocity = ", real_vel)
        self.curr_velocity = velocity
        self.debug_plotter.add(
            "real_vel_x", self.certain_position_update_time, np.array(real_vel[:2])[0]
        )
        self.debug_plotter.add(
            "vel_x", self.certain_position_update_time, self.curr_velocity[0]
        )
        self.debug_plotter.add(
            "real_vel_y", self.certain_position_update_time, np.array(real_vel[:2])[1]
        )
        self.debug_plotter.add(
            "vel_y", self.certain_position_update_time, self.curr_velocity[1]
        )

    def calculate_acceleration(self) -> np.array:
        """Calculates acceleration projected on horizontal plane"""
        angles = self.paddle.get_angles()
        print("angles = ", angles)
        gravity_forces = self.G * calculate_rotation(angles[0], angles[1])
        print("gravity forces = ", gravity_forces)
        return gravity_forces / self.M

    def new_velocity(self, velocity: np.array, time_delta: float) -> np.array:
        return velocity + self.calculate_acceleration() * time_delta

    def debug_plot(self):
        self.debug_plotter.plot_subplots(
            2, [["real_vel_x", "vel_x"], ["real_vel_y", "vel_y"]]
        )
