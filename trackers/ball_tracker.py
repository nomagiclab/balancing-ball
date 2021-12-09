from typing import List
from collections import deque

from ball.abc_ball import ABCBall
from paddle.abc_paddle import ABCPaddle

SMOOTHER_SIZE = 7
N = 3


class BallTracker:
    def __init__(self, ball: ABCBall, paddle: ABCPaddle):
        self.ball = ball
        self.paddle = paddle

        self.x_pos_list = deque(iterable=[ball.get_position()[0] for _ in range(SMOOTHER_SIZE)], maxlen=SMOOTHER_SIZE)
        self.dx_list = deque(iterable=[0 for _ in range(SMOOTHER_SIZE)], maxlen=SMOOTHER_SIZE)
        self.smooth_dx = 0

        self.y_pos_list = deque(iterable=[ball.get_position()[1] for _ in range(SMOOTHER_SIZE)], maxlen=SMOOTHER_SIZE)
        self.dy_list = deque(iterable=[0 for _ in range(SMOOTHER_SIZE)], maxlen=SMOOTHER_SIZE)
        self.smooth_dy = 0

    def get_error_vector(self) -> List[float]:
        ball_pos = self.ball.get_position()
        if self.paddle.check_if_in_range(ball_pos):
            paddle_pos = self.paddle.get_center_position()
            return [ball_pos - paddle_pos for ball_pos, paddle_pos in zip(ball_pos, paddle_pos)][:2]
        else:
            raise OutOfRange

    def update_smooth_derivative(self):
        ball_pos = self.ball.get_position()

        # Update the x positions.
        self.x_pos_list.pop()
        self.x_pos_list.appendleft(ball_pos[0])

        # Calculate the moving average value for dx.
        self.dx_list.pop()
        self.dx_list.appendleft(self.x_pos_list[0] - self.x_pos_list[1])
        self.smooth_dx = (N * self.smooth_dx - self.dx_list[N] + self.dx_list[0]) / N

        # Update the y positions.
        self.y_pos_list.pop()
        self.y_pos_list.appendleft(ball_pos[1])

        # Calculate the moving average value for dy
        self.dy_list.pop()
        self.dy_list.appendleft(self.y_pos_list[0] - self.y_pos_list[1])
        self.smooth_dy = (N * self.smooth_dy - self.dy_list[N] + self.dy_list[0]) / N

    def get_smooth_derivative(self) -> List[float]:
        return [self.smooth_dx, self.smooth_dy]

    def get_and_update_smooth_derivative(self) -> List[float]:
        self.update_smooth_derivative()
        return self.get_smooth_derivative()


class OutOfRange(Exception):
    pass
