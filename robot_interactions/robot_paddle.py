import math
from typing import List, Dict

from paddle.abc_paddle import ABCPaddle
from robot_interactions.robot_steering import Robot
from math import pi


def to_radians(angle):
    return angle * pi / 180


class RobotPaddle(ABCPaddle):
    MOVE_AXIS_INDEXES = {"x": 0, "y": 1, "z": 2}
    ROTATE_AXIS_INDEXES = {"x": 3, "y": 4, "z": 5}

    # https://www.dimensions.com/element/table-tennis-ping-pong-rackets-paddles
    # According to the website above diameter of ping pong paddle is 17cm.
    PADDLE_RADIUS_METERS = 0.17 / 2

    # INITIAL_JOINT_POSITION = [
    #     -1.6006999999999998,
    #     -1.7271,
    #     -2.2029999999999994,
    #     -0.8079999999999998,
    #     1.5951,
    #     -0.030999999999999694,
    # ]

    # INITIAL_JOINT_POSITION = [
    #     -1.5598993333333482,
    #     -1.7806993333333558,
    #     -1.9649986666666663,
    #     -0.9604642341667642,
    #     1.5951000000000002,
    #     -0.030999999999999694,
    # ]

    # INITIAL_JOINT_POSITION = [-pi / 2, -pi / 2, -pi / 2, -pi, -pi / 2, 0]

    # INITIAL_JOINT_POSITION = [-pi / 2, -pi / 2, -pi / 2, -pi, 0, 0]

    def __init__(
        self,
        ip_address,
        initial_joint_position=None,
    ):
        self.robot = Robot(ip_address)

        if initial_joint_position is not None:
            self.robot.move_joints_to_position(initial_joint_position)

        self.initial_joint_position = self.robot.get_joint_position()

        self.tcp_position = self.robot.get_tool_position()
        self.initial_tcp_position = self.tcp_position.copy()

        """[x, y, z, rx, ry, rz] where rx, ry, rz is in radians"""

    def set_angle_on_axis(self, axis: str, angle: float):
        print("Set angle on axis", axis, angle)
        self.tcp_position[self.ROTATE_AXIS_INDEXES[axis]] = (
            self.initial_tcp_position[self.ROTATE_AXIS_INDEXES[axis]]
            + to_radians(angle)
        ) % (2 * pi)
        self.robot.move_tool_smooth(self.tcp_position)

    def set_angle_on_axis_sync(self, axis: str, angle: float):
        print("Set angle on axis SYNC", axis, angle)
        self.tcp_position[self.ROTATE_AXIS_INDEXES[axis]] = (
            self.initial_tcp_position[self.ROTATE_AXIS_INDEXES[axis]]
            + to_radians(angle)
        ) % (2 * pi)
        self.robot.move_tool_sync(self.tcp_position)

    def rotate_around_axis(self, axis: str, angle: float):
        print("Rotate around axis", axis, angle)
        self.tcp_position[self.ROTATE_AXIS_INDEXES[axis]] += to_radians(angle)
        self.tcp_position[self.ROTATE_AXIS_INDEXES[axis]] %= 2 * pi
        self.robot.move_tool_smooth(self.tcp_position)

    def rotate_around_axis_sync(self, axis: str, angle: float):
        print("Rotate around axis SYNC", axis, angle)
        self.tcp_position[self.ROTATE_AXIS_INDEXES[axis]] += to_radians(angle)
        self.tcp_position[self.ROTATE_AXIS_INDEXES[axis]] %= 2 * pi
        self.robot.move_tool_sync(self.tcp_position)

    def move_by_vector(self, vector: List[float]):
        for index, axis in enumerate(["x", "y", "z"]):
            self.tcp_position[self.MOVE_AXIS_INDEXES[axis]] += vector[index]
        self.robot.move_tool_smooth(self.tcp_position)

    # Depraceted
    def move_to_position(self, position: List[float]):
        print("WARNING! depraceted method paddle.move_to_position used!")
        for index, axis in enumerate(["x", "y", "z"]):
            self.tcp_position[self.MOVE_AXIS_INDEXES[axis]] = position[index]
        self.robot.move_tool_smooth(self.tcp_position)

    def move_robot_to_position(self, position: List[float]):
        self.tcp_position = position
        self.robot.move_joints_to_position(position)
        self.initial_joint_position = self.get_joints_position()
        self.initial_tcp_position = self.get_center_position()

    def get_center_position(self) -> List[float]:
        return [
            self.tcp_position[self.MOVE_AXIS_INDEXES[axis]] for axis in ["x", "y", "z"]
        ]

    def get_center_orientation(self) -> Dict[str, float]:
        rotations = {}
        for axis, index in self.ROTATE_AXIS_INDEXES.items():
            rotations[axis] = self.tcp_position[index]
        return rotations

    def rotate_wrist(self, i, angle: float):
        pos = self.robot.get_joint_position()
        pos[i] += to_radians(angle)
        pos[i] %= 2 * pi
        self.robot.move_joints_to_position(pos)

    def get_joints_position(self) -> List[float]:
        return self.robot.get_joint_position()

    def check_if_in_range(self, position: List[float]) -> bool:
        # Heuristic, check if distance in x and y is not greater than
        # paddle radius
        distance_x_squared = (
            position[0] - self.tcp_position[self.MOVE_AXIS_INDEXES["x"]]
        ) ** 2
        distance_y_squared = (
            position[1] - self.tcp_position[self.MOVE_AXIS_INDEXES["y"]]
        ) ** 2

        return (
            distance_x_squared <= self.PADDLE_RADIUS_METERS**2
            and distance_y_squared <= self.PADDLE_RADIUS_METERS**2
        )

    def reset_torque_pos(self):
        self.robot.move_joints_to_position(self.initial_joint_position)

    def update_tcp_info(self):
        self.tcp_position = self.robot.get_tool_position()

    def stop(self):
        self.robot.stop()
