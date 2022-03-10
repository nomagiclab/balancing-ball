from typing import List
from paddle.abc_paddle import ABCPaddle
from paddle.paddle import Paddle
from robot_interactions.robot_paddle import RobotPaddle


class BiPaddle(ABCPaddle):
    def __init__(self, pybullet_paddle: Paddle, robot_paddle: RobotPaddle):
        self.pybullet_paddle = pybullet_paddle
        self.robot_paddle = robot_paddle

    def reset_position(self):
        self.pybullet_paddle.reset_position()
        self.robot_paddle.reset_torque_pos()

    def create_joint_controllers(self):
        self.pybullet_paddle.create_joint_controllers()

    def read_and_update_joint_position(self):
        self.pybullet_paddle.read_and_update_joint_position()

    def set_angle_on_axis(self, axis, angle):
        print("Rotation around axis: ", axis, " - ", angle)
        self.pybullet_paddle.set_angle_on_axis(axis, angle)
        self.robot_paddle.set_angle_on_axis(axis, angle)

    def rotate_around_axis(self, axis, angle):
        print("Rotation around axis: ", axis, " - ", angle)
        self.pybullet_paddle.rotate_around_axis(axis, angle)
        self.robot_paddle.rotate_around_axis(axis, angle)

    # Resets all the rotation angles on the paddle.
    def reset_torque_pos(self):
        self.pybullet_paddle.reset_torque_pos()
        self.robot_paddle.reset_torque_pos()

    def move_by_vector(self, vector: List[float], vel=1):
        self.pybullet_paddle.move_by_vector(vector, vel)
        self.robot_paddle.move_by_vector(vector)

    def move_to_position(self, position: List[float], vel=1):
        self.pybullet_paddle.move_to_position(position, vel)
        self.robot_paddle.move_to_position(position)

    def get_center_position(self) -> List[float]:
        return self.pybullet_paddle.get_center_position()

    def check_if_in_range(self, position: List[float]) -> bool:
        return self.pybullet_paddle.check_if_in_range(position)

    def steer_with_keyboard(self, rotation_speed, x_steering=[0], y_steering=[0]):
        self.pybullet_paddle.steer_with_keyboard(rotation_speed, x_steering, y_steering)
