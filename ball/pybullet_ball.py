from ball.abc_ball import ABCBall


class PybulletBall(ABCBall):
    MAX_HEIGHT = 2
    DEFAULT_ORIENTATION = [0, 0, 0, 1]
    DEFAULT_POSITION = [0.15, 0, 1]

    ROLLING_FRICTION = 0.0002
    SPINNING_FRICTION = 0.02
    LATERAL_FRICTION = 0.2
    RESTITUTION = 0.7
    MAX_ANGULAR_VELOCITY = 30

    def __init__(self, pybullet_client):
        super(PybulletBall, self).__init__()

        self.pybullet_client = pybullet_client

        self.id = pybullet_client.loadURDF("ball/ball.urdf", basePosition=self.DEFAULT_POSITION)
        pybullet_client.changeDynamics(self.id, -1, restitution=self.RESTITUTION,
                                       lateralFriction=self.LATERAL_FRICTION,
                                       spinningFriction=self.SPINNING_FRICTION,
                                       rollingFriction=self.ROLLING_FRICTION)

    def set_ball_angular_velocity(self, angular_velocity):
        self.pybullet_client.resetBaseVelocity(self.id, angularVelocity=angular_velocity)

    def set_position(self, position, orientation):
        self.pybullet_client.resetBasePositionAndOrientation(self.id, position, orientation)

    def get_position(self):
        return self.pybullet_client.getBasePositionAndOrientation(self.id)[0]
