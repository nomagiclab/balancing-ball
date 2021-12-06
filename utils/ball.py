#
from utils.button import Button


class Ball:
    MAX_HEIGHT = 2
    DEFAULT_ORIENTATION = [0, 0, 0, 1]
    DEFAULT_POSITION = [0.15, 0, 1]

    ROLLING_FRICTION = 0.0002
    SPINNING_FRICTION = 0.02
    LATERAL_FRICTION = 0.2
    RESTITUTION = 0.7
    MAX_ANGULAR_VELOCITY = 30

    def __init__(self, p):
        self.id = p.loadURDF("urdf_models/ball.urdf", basePosition=self.DEFAULT_POSITION)
        p.changeDynamics(self.id, -1, restitution=self.RESTITUTION,
                         lateralFriction=self.LATERAL_FRICTION,
                         spinningFriction=self.SPINNING_FRICTION,
                         rollingFriction=self.ROLLING_FRICTION)

        self.set_rotation_sliders = [p.addUserDebugParameter("Angular velocity x",
                                                             -self.MAX_ANGULAR_VELOCITY, self.MAX_ANGULAR_VELOCITY, 0),
                                     p.addUserDebugParameter("Angular velocity y",
                                                             -self.MAX_ANGULAR_VELOCITY, self.MAX_ANGULAR_VELOCITY, 0),
                                     p.addUserDebugParameter("Angular velocity z",
                                                             -self.MAX_ANGULAR_VELOCITY, self.MAX_ANGULAR_VELOCITY, 0)]

        self.set_ball_height_slider = p.addUserDebugParameter("Set initial ball height", 0,
                                                              self.MAX_HEIGHT,
                                                              self.DEFAULT_POSITION[2])
        self.set_ball_height_button = Button(p.addUserDebugParameter("Drop ball with rotation", 1, 0, 0))

        self.set_rotation_button = Button(p.addUserDebugParameter("Set rotation without changing position", 1, 0, 0))

    def _set_ball_angular_velocity(self, p, angular_velocity):
        print("setting angular velocity to", angular_velocity)
        p.resetBaseVelocity(self.id, angularVelocity=angular_velocity)

    def reset_ball_position(self, p, height):
        p.resetBasePositionAndOrientation(self.id, [self.DEFAULT_POSITION[0], self.DEFAULT_POSITION[1], height],
                                          self.DEFAULT_ORIENTATION)

    def check_and_update_height(self, p):
        if self.set_ball_height_button.was_clicked():
            self.reset_ball_position(p, p.readUserDebugParameter(self.set_ball_height_slider))
            self._set_ball_angular_velocity(p, [p.readUserDebugParameter(i) for i in self.set_rotation_sliders])

    def check_and_update_rotation(self, p):
        if self.set_rotation_button.was_clicked():
            self._set_ball_angular_velocity(p, [p.readUserDebugParameter(i) for i in self.set_rotation_sliders])