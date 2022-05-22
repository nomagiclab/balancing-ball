from collections import deque

N = 3


# Calculates mean of last N derivatives.
class DerivativeCalculator:
    def __init__(self):
        # Value doesn't matter as we won't use it.
        self.last_x = None

        self.last_time = 0

        self.dx_list = deque(iterable=[0 for _ in range(N + 1)], maxlen=N + 1)

        # curr_dx is always equal to mean of _N last dxs.
        self.curr_dx = 0

    def update_derivative(self, new_x, new_time):
        # Update dx list.
        self.dx_list.pop()

        if self.last_time == 0:
            self.last_time = new_time

        if self.last_time != new_time:
            self.dx_list.appendleft((new_x - self.last_x) / (new_time - self.last_time))
        else:
            self.dx_list.appendleft(0)

        # Calculate moving average of last _N dx.
        self.curr_dx = self.curr_dx + (self.dx_list[0] - self.dx_list[N]) / N

        self.last_x = new_x
        self.last_time = new_time

    # THIS IS A LEGACY VERSION OF THE
    # def update_derivative(self, new_x, new_time):
    #     if self.last_time == 0:
    #         self.last_time = new_time
    #
    #     if self.last_time != new_time:
    #         self.curr_dx = (self.last_x - new_x) / (new_time - self.last_time)
    #
    #     self.last_x = new_x
    #     self.last_time = new_time

    def get_current_derivative(self) -> float:
        return self.curr_dx

    def get_and_update_derivative(self, new_x, new_time) -> float:
        self.update_derivative(new_x, new_time)
        return self.get_current_derivative()
