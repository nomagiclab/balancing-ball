from typing import List

from ball.abc_ball import ABCBall


DEFAULT_POSITION = [0, 0, 1]
DEFAULT_ORIENTATION = [0, 0, 0, 1]
MAX_HEIGHT = 2

ROLLING_FRICTION = 0.0002
SPINNING_FRICTION = 0.02
LATERAL_FRICTION = 0.2
RESTITUTION = 0.7
MAX_ANGULAR_VELOCITY = 60


class PyBulletBall(ABCBall):
    def __init__(self, pybullet_client):
        super(PyBulletBall, self).__init__()

        self.pybullet_client = pybullet_client

        self.id = pybullet_client.loadURDF(
            "ball/ball.urdf", basePosition=DEFAULT_POSITION
        )
        pybullet_client.changeDynamics(
            self.id,
            -1,
            restitution=RESTITUTION,
            lateralFriction=LATERAL_FRICTION,
            spinningFriction=SPINNING_FRICTION,
            rollingFriction=ROLLING_FRICTION,
        )

    def set_ball_angular_velocity(self, angular_velocity):
        self.pybullet_client.resetBaseVelocity(
            self.id, angularVelocity=angular_velocity
        )

    def set_position(self, position, orientation):
        self.pybullet_client.resetBasePositionAndOrientation(
            self.id, position, orientation
        )

    def set_velocity(self, velocity: List[float]):
        self.pybullet_client.resetBaseVelocity(self.id, linearVelocity=velocity)

    def get_position(self) -> List[float]:
        return self.pybullet_client.getBasePositionAndOrientation(self.id)[0]
