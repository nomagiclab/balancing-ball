import pybullet as p


class Button:
    def __init__(self, buttonId: int):
        self.id = buttonId
        self.counter = 0

    # returns True if button was clicked since the last time
    # wasClicked returned True.
    def wasClicked(self) -> bool:
        if p.readUserDebugParameter(self.id) > self.counter:
            self.counter = p.readUserDebugParameter(self.id)
            return True
        return False
