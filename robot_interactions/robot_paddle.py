import numpy as np
import math
import cv2

from scipy.spatial.transform import Rotation as R
from typing import List, Dict

from paddle.abc_paddle import ABCPaddle
from robot_interactions.robot_steering import Robot


class RobotPaddle(ABCPaddle):
    # TODO
    def get_angles(self) -> List[float]:
        raise NotImplementedError

    MOVE_AXIS_INDEXES = {"x": 0, "y": 1, "z": 2}
    ROTATE_AXIS_INDEXES = {"x": 3, "y": 4, "z": 5}

    # https://www.dimensions.com/element/table-tennis-ping-pong-rackets-paddles
    # According to the website above diameter of ping pong paddle is 17cm.
    PADDLE_RADIUS_METERS = 0.17 / 2

    INITIAL_POSE = [
        0.7515497250864069,
        -0.1073135360489473,
        0.16513409510172675,
        -0.009236061555885475,
        1.5514308949914648,
        0.06449220849435575,
    ]

    INITIAL_Q = [
        0.01856282353401184,
        -1.725330492059225,
        -2.404684543609619,
        -2.1323920689024867,
        -1.5921157042132776,
        4.754701137542725,
    ]

    def __init__(
        self,
        ip_address,
        initial_joint_position=None,
    ):
        self.robot = Robot(ip_address)

        if initial_joint_position is None:
            self.robot.set_tcp([0, 0, 0.366, 0, 0, 0])
            self.robot.moveJ(RobotPaddle.INITIAL_Q)
            # TODO - tbh nie wiem co to jest za pozycja, nie moge znalezc opcji ktora by zwracała dokładnie taką.
            self.initial_pose = RobotPaddle.INITIAL_POSE

    @staticmethod
    def __create_givens(theta):
        return np.array(
            [
                [math.cos(theta), 0.0, math.sin(theta)],
                [0.0, 1.0, 0.0],
                [-math.sin(theta), 0.0, math.cos(theta)],
            ]
        )

    def set_angles_rp(self, roll, pitch):
        rotation_matrix = self.__create_givens(math.radians(-90))

        joint_angles = np.array(
            [
                self.initial_pose[3],
                -self.initial_pose[4],
                -self.initial_pose[5],
            ]
        )

        # Convert the joint rotation angles vector, to a rotation matrix.
        rmat, _ = cv2.Rodrigues(joint_angles)
        rmat = rotation_matrix.T.dot(rmat)

        # Convert the angles to the rpy format.
        rpy = R.from_matrix(rmat).as_euler("xyz")
        rpy[1] = pitch
        rpy[2] = -roll

        # Convert back the rpy angles to the robot joint angles system.
        rmat = R.from_euler("xyz", rpy).as_matrix()
        rmat = rotation_matrix.dot(rmat)
        rvec, _ = cv2.Rodrigues(rmat)
        rvec = [rvec[0], -rvec[1], -rvec[2]]

        # Update the correct robot pose.
        pose = self.initial_pose.copy()
        pose[3:] = rvec

        # Calculate the IK solution, for the new pose.
        p = self.robot.rtde_c.getInverseKinematics(pose)

        # Move the robot to the new pose.
        self.robot.servoJ(p)

    def set_angles(self, x_angle: float, y_angle: float):
        self.set_angles_rp(x_angle, y_angle)

    def reset_torque_pos(self):
        self.robot.moveJ(RobotPaddle.INITIAL_Q)

    # ----------NOT CRUCIAL METHODS
    # def rotate_around_axis(self, axis: str, angle: float):
    #     print("Rotate around axis", axis, angle)
    #     self.tcp_position[self.ROTATE_AXIS_INDEXES[axis]] += math.radians(angle)
    #     self.tcp_position[self.ROTATE_AXIS_INDEXES[axis]] %= 2 * math.pi
    #     self.robot.servoL(self.tcp_position)
    #
    # def rotate_around_axis_sync(self, axis: str, angle: float):
    #     print("Rotate around axis SYNC", axis, angle)
    #     self.tcp_position[self.ROTATE_AXIS_INDEXES[axis]] += math.radians(angle)
    #     self.tcp_position[self.ROTATE_AXIS_INDEXES[axis]] %= 2 * math.pi
    #     self.robot.moveL(self.tcp_position)

    # def move_by_vector(self, vector: List[float]):
    #     for index, axis in enumerate(["x", "y", "z"]):
    #         self.tcp_position[self.MOVE_AXIS_INDEXES[axis]] += vector[index]
    #     self.robot.servoL(self.tcp_position)

    # # Depraceted
    # def move_to_position(self, position: List[float]):
    #     print("WARNING! depraceted method paddle.move_to_position used!")
    #     for index, axis in enumerate(["x", "y", "z"]):
    #         self.tcp_position[self.MOVE_AXIS_INDEXES[axis]] = position[index]
    #     self.robot.servoL(self.tcp_position)

    # def move_robot_to_position(self, position: List[float]):
    #     self.tcp_position = position
    #     self.robot.moveJ(position)
    #     self.initial_joint_position = self.get_joints_position()
    #     self.initial_tcp_position = self.get_center_position()

    # def set_angle_on_axis_moveL(self, axis: str, angle: float):
    #     print("Set angle on axis SYNC", axis, angle)
    #     self.tcp_position[self.ROTATE_AXIS_INDEXES[axis]] = (
    #         self.initial_tcp_position[self.ROTATE_AXIS_INDEXES[axis]]
    #         + math.radians(angle)
    #     ) % (2 * math.pi)
    #     self.robot.moveL(self.tcp_position)
    #
    # def get_center_position(self) -> List[float]:
    #     return [
    #         self.tcp_position[self.MOVE_AXIS_INDEXES[axis]] for axis in ["x", "y", "z"]
    #     ]
    #
    # def get_center_orientation(self) -> Dict[str, float]:
    #     rotations = {}
    #     for axis, index in self.ROTATE_AXIS_INDEXES.items():
    #         rotations[axis] = self.tcp_position[index]
    #     return rotations
    #
    # def rotate_wrist(self, i, angle: float):
    #     pos = self.robot.get_joint_position()
    #     pos[i] += math.radians(angle)
    #     pos[i] %= 2 * math.pi
    #     self.robot.moveJ(pos)

    # def check_if_in_range(self, position: List[float]) -> bool:
    #     # Heuristic, check if distance in x and y is not greater than
    #     # paddle radius
    #     distance_x_squared = (
    #         position[0] - self.tcp_position[self.MOVE_AXIS_INDEXES["x"]]
    #     ) ** 2
    #     distance_y_squared = (
    #         position[1] - self.tcp_position[self.MOVE_AXIS_INDEXES["y"]]
    #     ) ** 2
    #
    #     return (
    #         distance_x_squared <= self.PADDLE_RADIUS_METERS**2
    #         and distance_y_squared <= self.PADDLE_RADIUS_METERS**2
    #     )

    def stop(self):
        self.robot.stop()

    # def get_joints_position(self) -> List[float]:
    #     return self.robot.get_joint_position()
    #
    #
    # def update_tcp_info(self):
    #     self.tcp_position = self.robot.get_tool_position()
