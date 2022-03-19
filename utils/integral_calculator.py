class IntegralCalculator:
    def __init__(self):
        self.value = 0
        self.last_time = 0

    def get_current_integral(self) -> float:
        return self.value

    def get_and_update_integral(self, new_x, new_time) -> float:
        self.update_integral(new_x, new_time)
        return self.get_current_integral()

    def update_integral(self, new_x, new_time):
        if self.last_time == 0:
            self.last_time = new_time

        dt = new_time - self.last_time

        self.value += dt * new_x

        self.last_time = new_time
