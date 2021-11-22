from abc_paddle import ABCPaddle


class OnlyPaddle(ABCPaddle):
    urdf_model = 'paddle.urdf'

    # The following are the paddle important joints ids.
    # These are hard coded values, so always make sure to check these after changing paddle urdf model.
    move_axis_joints = {'x': 2, 'y': 1, 'z': 0}
    rotate_axis_joints = {'x': 3, 'y': 4, 'z': 5}

    def __init__(self, pybullet_client):
        super().__init__(pybullet_client)
        self.pybullet_client.changeDynamics(self.robot_id, -1, mass=0.0)

        # Set the friction and restitution of the paddle.
        self.pybullet_client.changeDynamics(self.robot_id, 6, lateralFriction=0.1, restitution=0.7)

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
