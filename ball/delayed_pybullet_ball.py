from abc import ABC
from collections import deque
from typing import List

from ball.abc_ball import ABCBall
from ball.pybullet_ball import PyBulletBall


class DelayedPybulletBall(ABCBall):
    def __init__(self, ball: PyBulletBall, n_delayed, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ball = ball
        self.n_delayed = n_delayed
        self.positions_q = deque(maxlen=n_delayed)

    def get_position(self) -> List[float]:
        ret = self.positions_q[0]
        self.positions_q.append(self.ball.get_position())
        return ret
