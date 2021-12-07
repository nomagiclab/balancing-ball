import typing

from paddle.abc_paddle import ABCPaddle


class Paddle(ABCPaddle):
    urdf_model = 'paddle/paddle.urdf'

    # The following are the paddle important joints ids.
    # These are hard coded values, so always make sure to check these after changing paddle urdf model.
    MOVE_AXIS_JOINTS = {'x': 2, 'y': 1, 'z': 0}
    ROTATE_AXIS_JOINTS = {'x': 5, 'y': 4, 'z': 3}
    PADDLE_LINK_ID = 5

    joint_controllers = typing.List[int]

    def __init__(self, pybullet_client):
        super().__init__(pybullet_client)
        self.joint_ids = [i for i in range(0, 6)]
        self.pybullet_client.changeDynamics(self.robot_id, -1, mass=0.0)

        # Set the friction and restitution of the paddle.
        self.pybullet_client.changeDynamics(self.robot_id, 6, lateralFriction=0.01, restitution=0.7)

    def reset_position(self):
        self.pybullet_client.resetBasePositionAndOrientation(self.robot_id, [0, 0, 0], [0, 0, 0, 1])

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
        joint_pos = self.pybullet_client.getJointState(self.robot_id, self.ROTATE_AXIS_JOINTS[axis])[0]

        self.pybullet_client.setJointMotorControl2(self.robot_id,
                                                   self.ROTATE_AXIS_JOINTS[axis],
                                                   self.pybullet_client.POSITION_CONTROL,
                                                   targetPosition=joint_pos + angle * 3.14 / 180)

    def move_by_vector(self, v, vel=1):
        axes = ['x', 'y', 'z']

        for i in range(3):
            joint_pos = self.pybullet_client.getJointState(self.robot_id, self.MOVE_AXIS_JOINTS[axes[i]])[0]

            self.pybullet_client.setJointMotorControl2(self.robot_id,
                                                       self.MOVE_AXIS_JOINTS[axes[i]],
                                                       self.pybullet_client.POSITION_CONTROL,
                                                       targetPosition=joint_pos + v[i],
                                                       maxVelocity=vel)

    def move_to_position(self, p, vel=1):
        axes = ['x', 'y', 'z']

        for i in range(3):
            self.pybullet_client.setJointMotorControl2(self.robot_id,
                                                       self.MOVE_AXIS_JOINTS[axes[i]],
                                                       self.pybullet_client.POSITION_CONTROL,
                                                       targetPosition=p[i],
                                                       maxVelocity=vel)

    def get_center_position(self):
        return self.pybullet_client.getLinkState(self.robot_id, self.PADDLE_LINK_ID)[0]

    def steer_with_keyboard(self, rotation_speed, x_steering=[0], y_steering=[0]):
        p = self.pybullet_client
        keys = p.getKeyboardEvents()

        # handle keyboard events
        for k, v in keys.items():
            if k == p.B3G_RIGHT_ARROW and (v & p.KEY_WAS_TRIGGERED):
                x_steering[0] = -1
            if k == p.B3G_RIGHT_ARROW and (v & p.KEY_WAS_RELEASED):
                x_steering[0] = 0

            if k == p.B3G_LEFT_ARROW and (v & p.KEY_WAS_TRIGGERED):
                x_steering[0] = 1
            if k == p.B3G_LEFT_ARROW and (v & p.KEY_WAS_RELEASED):
                x_steering[0] = 0

            if k == p.B3G_UP_ARROW and (v & p.KEY_WAS_TRIGGERED):
                y_steering[0] = 1
            if k == p.B3G_UP_ARROW and (v & p.KEY_WAS_RELEASED):
                y_steering[0] = 0

            if k == p.B3G_DOWN_ARROW and (v & p.KEY_WAS_TRIGGERED):
                y_steering[0] = -1
            if k == p.B3G_DOWN_ARROW and (v & p.KEY_WAS_RELEASED):
                y_steering[0] = 0

        self.rotate_around_axis('x', x_steering[0] * rotation_speed)
        self.rotate_around_axis('y', y_steering[0] * rotation_speed)
