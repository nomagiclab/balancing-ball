import queue
import threading
from collections import deque
from typing import List

from ball.abc_ball import ABCBall
from paddle.paddle import Paddle
from position_prediction.abc_predicter import ABCPredicter
from trackers.abstract_tracker import OutOfRange, AbstractBallTracker
from utils.non_blocking_put_queue import NonBlockingPutQueue


class ConcurrentPredictingBallTracker(AbstractBallTracker):
    def __init__(
        self,
        ball: ABCBall,
        paddle: Paddle,
        n_predict: int,
        prediction_index: int,
        predicter: ABCPredicter,
        fetch_time: float,
    ):
        self.last_position = NonBlockingPutQueue(maxsize=1)
        self.ball = ball
        self.paddle = paddle
        self.prediction_index = prediction_index
        self.m_queue = deque(maxlen=n_predict)
        self.predicter = predicter
        self.fetch_time = fetch_time
        self.get_position_in_loop()

    def get_position_in_loop(self):
        self.last_position.put(self.ball.get_position())
        threading.Timer(self.fetch_time, self.get_position_in_loop).start()

    def __get_error_from_position(self, ball_pos: List[float]):
        if self.paddle.check_if_in_range(ball_pos):
            paddle_pos = self.paddle.get_center_position()
            return [
                ball_pos - paddle_pos
                for ball_pos, paddle_pos in zip(ball_pos, paddle_pos)
            ][:2]
        else:
            raise OutOfRange

    def get_error_vector(self) -> List[float]:
        ball_pos: List[float]
        try:
            ball_pos = self.last_position.get_nowait()
            self.m_queue.append(ball_pos)
        except queue.Empty:
            ball_pos = list(
                self.predicter.predict_x_y(list(self.m_queue), self.prediction_index)
            )

        return self.__get_error_from_position(ball_pos)

    def get_ball_position(self) -> List[float]:
        return self.ball.get_position()
