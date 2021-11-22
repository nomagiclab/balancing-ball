import typing
from paddle.abc_paddle import ABCPaddle


class OnlyPaddle(ABCPaddle):
    urdf_model = 'paddle/paddle.urdf'

    # The following are the paddle important joints ids.
    # These are hard coded values, so always make sure to check these after changing paddle urdf model.
    move_axis_joints = {'x': 2, 'y': 1, 'z': 0}
    rotate_axis_joints = {'x': 5, 'y': 4, 'z': 3}
    joint_controllers = typing.List[int]

    def __init__(self, pybullet_client):
        super().__init__(pybullet_client)
        self.joint_ids = [i for i in range(0, 6)]
        self.pybullet_client.changeDynamics(self.robot_id, -1, mass=0.0)

        # Set the friction and restitution of the paddle.
        self.pybullet_client.changeDynamics(self.robot_id, 6, lateralFriction=0.01, restitution=0.7)

    def create_joint_controllers(self):
        self.joint_controllers = []

        self.joint_controllers.append(self.pybullet_client.addUserDebugParameter("z", 0, 3, 0.5))
        self.joint_controllers.append(self.pybullet_client.addUserDebugParameter("y", -1, 1, 0))
        self.joint_controllers.append(self.pybullet_client.addUserDebugParameter("x", -1, 1, 0))
        self.joint_controllers.append(self.pybullet_client.addUserDebugParameter("z_roll", -3.14, 3.14, 0))
        self.joint_controllers.append(self.pybullet_client.addUserDebugParameter("y_roll", -3.14, 3.14, 0))
        self.joint_controllers.append(self.pybullet_client.addUserDebugParameter("x_roll", -3.14, 3.14, 0))

    def read_and_update_joint_position(self):
        for i in range(len(self.joint_controllers)):
            self.pybullet_client.setJointMotorControl2(self.robot_id,
                                                       i,
                                                       self.pybullet_client.POSITION_CONTROL,
                                                       self.pybullet_client.readUserDebugParameter(
                                                           self.joint_controllers[i]))

    def rotate_around_axis(self, axis, angle):
        joint_pos = self.pybullet_client.getJointState(self.robot_id, self.rotate_axis_joints[axis])[0]

        self.pybullet_client.setJointMotorControl2(self.robot_id,
                                                   self.rotate_axis_joints[axis],
                                                   self.pybullet_client.POSITION_CONTROL,
                                                   targetPosition=joint_pos + angle * 3.14 / 180)

    def move_by_vector(self, v):
        pass

    def move_to_position(self, p):
        pass
