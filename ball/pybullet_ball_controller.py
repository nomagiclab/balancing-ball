from typing import List

from ball.pybullet_ball import PyBulletBall
import ball.pybullet_ball as pybullet_ball
from utils.button import Button
from utils.physics import get_force_vector
from paddle.paddle import PADDLE_RADIUS_M


class PyBulletBallController:
    def __init__(self, ball: PyBulletBall):
        self.pybullet_client = ball.pybullet_client
        self._ball = ball

        self._set_rotation_sliders = [
            self.pybullet_client.addUserDebugParameter(
                "Angular velocity x",
                -pybullet_ball.MAX_ANGULAR_VELOCITY,
                pybullet_ball.MAX_ANGULAR_VELOCITY,
                0,
            ),
            self.pybullet_client.addUserDebugParameter(
                "Angular velocity y",
                -pybullet_ball.MAX_ANGULAR_VELOCITY,
                pybullet_ball.MAX_ANGULAR_VELOCITY,
                0,
            ),
            self.pybullet_client.addUserDebugParameter(
                "Angular velocity z",
                -pybullet_ball.MAX_ANGULAR_VELOCITY,
                pybullet_ball.MAX_ANGULAR_VELOCITY,
                0,
            ),
        ]

        self._set_initial_position_sliders = [
            self.pybullet_client.addUserDebugParameter(
                "position x",
                -PADDLE_RADIUS_M,
                PADDLE_RADIUS_M,
                0,
            ),
            self.pybullet_client.addUserDebugParameter(
                "position y",
                -PADDLE_RADIUS_M,
                PADDLE_RADIUS_M,
                0,
            ),
        ]
        self._set_ball_height_slider = self.pybullet_client.addUserDebugParameter(
            "Set initial ball height",
            0,
            pybullet_ball.MAX_HEIGHT,
            pybullet_ball.DEFAULT_POSITION[2],
        )
        self._set_ball_height_button = Button(
            self.pybullet_client.addUserDebugParameter(
                "Drop ball with rotation", 1, 0, 0
            )
        )

        self._set_rotation_button = Button(
            self.pybullet_client.addUserDebugParameter(
                "Set rotation without changing position", 1, 0, 0
            )
        )

        self._throw_ball_button = Button(
            self.pybullet_client.addUserDebugParameter(
                "Throw ball towards paddle", 1, 0, 0
            )
        )

    def check_if_drop_with_rotation(self):
        if self._set_ball_height_button.was_clicked():
            self._reset_ball_position(
                self.pybullet_client.readUserDebugParameter(
                    self._set_ball_height_slider
                ),
                self.pybullet_client.readUserDebugParameter(
                    self._set_initial_position_sliders[0]
                ),
                self.pybullet_client.readUserDebugParameter(
                    self._set_initial_position_sliders[1]
                ),
            )
            self._ball.set_ball_angular_velocity(
                [
                    self.pybullet_client.readUserDebugParameter(i)
                    for i in self._set_rotation_sliders
                ]
            )

    def check_and_update_rotation(self):
        if self._set_rotation_button.was_clicked():
            self._ball.set_ball_angular_velocity(
                [
                    self.pybullet_client.readUserDebugParameter(i)
                    for i in self._set_rotation_sliders
                ]
            )

    def _reset_ball_position(
        self,
        height: float,
        x: float = pybullet_ball.DEFAULT_POSITION[0],
        y: float = pybullet_ball.DEFAULT_POSITION[1],
    ):
        self._ball.set_position(
            [x, y, height],
            pybullet_ball.DEFAULT_ORIENTATION,
        )
        self._ball.set_velocity([0, 0, 0])

    def should_throw_ball(self) -> bool:
        return self._throw_ball_button.was_clicked()

    def throw_ball(self, position: List[float]):
        assert len(position) == 3

        vec = get_force_vector(self._ball.get_position(), position)
        self.pybullet_client.applyExternalForce(
            self._ball.id, -1, vec, [0, 0, 0], self.pybullet_client.WORLD_FRAME
        )
