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
        self.discarded_queue = deque()
        self.predicted_on_q = 0
        self.predicter = predicter
        self.fetch_time = fetch_time
        self.get_position_in_loop()
        self.__last_predicted_pos = None

    @property
    def last_predicted_pos(self):
        return self.__last_predicted_pos

    @last_predicted_pos.getter
    def last_predicted_pos(self):
        res = self.__last_predicted_pos
        self.__last_predicted_pos = None
        return res

    def get_position_in_loop(self):
        self.last_position.put(self.ball.get_position())

        ball_thread = threading.Timer(self.fetch_time, self.get_position_in_loop)
        ball_thread.daemon = True
        ball_thread.start()

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
            # Remove all the predicted values from the queue.
            if len(self.discarded_queue) > 0:
                for _ in range(self.predicted_on_q):
                    self.m_queue.pop()
                self.predicted_on_q = 0
                # Restore all the discarded real values.
                self.m_queue.extendleft(self.discarded_queue)
                self.discarded_queue.clear()

        except queue.Empty:
            self.__last_predicted_pos = list(
                self.predicter.predict_x_y(list(self.m_queue), self.prediction_index)
            )
            ball_pos = self.__last_predicted_pos

            self.predicted_on_q += 1
            # If the queue is full, save the oldest value so we can restore it later.
            if len(self.m_queue) == self.m_queue.maxlen:
                self.discarded_queue.appendleft(self.m_queue.popleft())

        self.m_queue.append(ball_pos)

        return self.__get_error_from_position(ball_pos)

    def get_ball_position(self) -> List[float]:
        return self.ball.get_position()


class ConcurrentPredictingBallTrackerNoDiscard(ConcurrentPredictingBallTracker):
    def get_error_vector(self) -> List[float]:
        ball_pos: List[float]
        try:
            ball_pos = self.last_position.get_nowait()

        except queue.Empty:
            self.__last_predicted_pos = list(
                self.predicter.predict_x_y(list(self.m_queue), self.prediction_index)
            )
            ball_pos = self.__last_predicted_pos

        self.m_queue.append(ball_pos)

        return self.__get_error_from_position(ball_pos)
