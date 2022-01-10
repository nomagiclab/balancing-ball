from collections import deque

N = 3
SMOOTHER_SIZE = 7


class DerivativeCalculator:
    def __init__(self, initial_position):
        self.pos_list = deque(iterable=[initial_position for _ in range(SMOOTHER_SIZE)], maxlen=SMOOTHER_SIZE)
        self.dx_list = deque(iterable=[0 for _ in range(SMOOTHER_SIZE)], maxlen=SMOOTHER_SIZE)
        self.curr_dx = 0

    def update_derivative(self, pos):
        # Update the current position values.
        self.pos_list.pop()
        self.pos_list.appendleft(pos)

        # Calculate the moving average value for dx.
        self.dx_list.pop()
        self.dx_list.appendleft(self.pos_list[0] - self.pos_list[1])
        self.curr_dx = (N * self.curr_dx - self.dx_list[N] + self.dx_list[0]) / N

    def get_current_derivative(self) -> float:
        return self.curr_dx

    def get_and_update_derivative(self, pos) -> float:
        self.update_derivative(pos)
        return self.get_current_derivative()
