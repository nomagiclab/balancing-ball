from typing import List

from ball.abc_ball import ABCBall
from paddle.paddle import Paddle
from trackers.abstract_tracker import AbstractBallTracker, OutOfRange

SMOOTHER_SIZE = 7
N = 3


class BallTracker(AbstractBallTracker):
    def __init__(self, ball: ABCBall, paddle: Paddle):
        self.ball = ball
        self.paddle = paddle
        self.last_predicted_pos = [0, 0, 0]

    def get_error_vector(self) -> List[float]:
        ball_pos = self.ball.get_position()
        if self.paddle.check_if_in_range(ball_pos):
            paddle_pos = self.paddle.get_center_position()
            return [
                ball_pos - paddle_pos
                for ball_pos, paddle_pos in zip(ball_pos, paddle_pos)
            ][:2]
        else:
            raise OutOfRange

    def get_ball_position(self) -> List[float]:
        return self.ball.get_position()
