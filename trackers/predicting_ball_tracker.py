from collections import deque
from typing import List

from ball.delayed_pybullet_ball import DelayedPybulletBall
from ball.pybullet_ball import PyBulletBall
from paddle.paddle import Paddle
from position_prediction.abc_predicter import ABCPredicter
from position_prediction.polynomial_interpolation import PolynomialPredicter
from trackers.abstract_tracker import OutOfRange, AbstractBallTracker


class PredictingBallTracker(AbstractBallTracker):
    def __init__(
        self,
        ball: DelayedPybulletBall,
        paddle: Paddle,
        n_predict: int,
        prediction_index: int,
        predicter: ABCPredicter,
    ):
        self.ball = ball
        self.paddle = paddle
        self.prediction_index = prediction_index
        self.m_queue = deque(maxlen=n_predict)
        self.predicter = predicter

    def get_error_vector(self) -> List[float]:
        self.m_queue.append(tuple(self.ball.get_position()))

        ball_pos = list(
            self.predicter.predict_x_y(list(self.m_queue), self.prediction_index)
        )

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
