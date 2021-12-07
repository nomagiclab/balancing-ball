from typing import List

from ball.pybullet_ball import PybulletBall
from utils.button import Button
from utils.physics import get_force_vector


class PybulletBallController:
    def __init__(self, ball: PybulletBall):
        self.__pybullet_client = ball.pybullet_client
        self.__ball = ball

        self.__set_rotation_sliders = [self.__pybullet_client.addUserDebugParameter("Angular velocity x",
                                                                                    -ball.MAX_ANGULAR_VELOCITY,
                                                                                    ball.MAX_ANGULAR_VELOCITY, 0),
                                       self.__pybullet_client.addUserDebugParameter("Angular velocity y",
                                                                                    -ball.MAX_ANGULAR_VELOCITY,
                                                                                    ball.MAX_ANGULAR_VELOCITY, 0),
                                       self.__pybullet_client.addUserDebugParameter("Angular velocity z",
                                                                                    -ball.MAX_ANGULAR_VELOCITY,
                                                                                    ball.MAX_ANGULAR_VELOCITY, 0)]

        self.__set_ball_height_slider = self.__pybullet_client.addUserDebugParameter("Set initial ball height", 0,
                                                                                     ball.MAX_HEIGHT,
                                                                                     ball.DEFAULT_POSITION[2])
        self.__set_ball_height_button = Button(
            self.__pybullet_client.addUserDebugParameter("Drop ball with rotation", 1, 0, 0))

        self.__set_rotation_button = Button(
            self.__pybullet_client.addUserDebugParameter("Set rotation without changing position", 1, 0, 0))

        self.__throw_ball_button = Button(
            self.__pybullet_client.addUserDebugParameter("Throw ball towards paddle", 1, 0, 0))

    def check_if_drop_with_rotation(self):
        if self.__set_ball_height_button.was_clicked():
            self._reset_ball_position(self.__pybullet_client.readUserDebugParameter(self.__set_ball_height_slider))
            self.__ball.set_ball_angular_velocity(
                [self.__pybullet_client.readUserDebugParameter(i) for i in self.__set_rotation_sliders])

    def check_and_update_rotation(self):
        if self.__set_rotation_button.was_clicked():
            self.__ball.set_ball_angular_velocity([self.__pybullet_client.readUserDebugParameter(i)
                                                   for i in self.__set_rotation_sliders])

    def _reset_ball_position(self, height: float):
        self.__ball.set_position([self.__ball.DEFAULT_POSITION[0], self.__ball.DEFAULT_POSITION[1], height],
                                 self.__ball.DEFAULT_ORIENTATION)

    def should_throw_ball(self) -> bool:
        return self.__throw_ball_button.was_clicked()

    def throw_ball(self, position: List[float]):
        assert len(position) == 3

        vec = get_force_vector(self.__ball.get_position(), position)
        self.__pybullet_client.applyExternalForce(self.__ball.id, -1, vec, [0, 0, 0],
                                                  self.__pybullet_client.WORLD_FRAME)
