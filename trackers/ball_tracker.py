from typing import List

from ball.abc_ball import ABCBall
from paddle.abc_paddle import ABCPaddle
from virtualcam.virtualcam import VirtualCam

SMOOTHER_SIZE = 7
N = 3


class BallTracker:
    def __init__(self, ball: ABCBall, paddle: ABCPaddle, virtualcam: VirtualCam):
        self.ball = ball
        self.paddle = paddle
        self.virtualcam = virtualcam

    def get_error_vector2(self) -> List[float]:
        ball_pos = self.ball.get_position()
        if self.paddle.check_if_in_range(ball_pos):
            paddle_pos = self.paddle.get_center_position()
            return [
                ball_pos - paddle_pos
                for ball_pos, paddle_pos in zip(ball_pos, paddle_pos)
            ][:2]
        else:
            raise OutOfRange

    def get_error_vector(self) -> List[float]:
        ball_pos, paddle_pos = self.virtualcam.get_objects_location()
        if self.paddle.check_if_in_range(ball_pos):
            return [
                ball_pos - paddle_pos
                for ball_pos, paddle_pos in zip(ball_pos, paddle_pos)
            ][:2]
        else:
            raise OutOfRange    

    def get_ball_position(self) -> List[float]:
        return self.ball.get_position()


class OutOfRange(Exception):
    pass
