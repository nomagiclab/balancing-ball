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
        new_position = self.ball.get_position()
        ret = self.positions_q[0] if len(self.positions_q) > 0 else new_position
        # print("Real ball position", new_position, "Returned position", ret)
        self.positions_q.append(new_position)
        return ret
