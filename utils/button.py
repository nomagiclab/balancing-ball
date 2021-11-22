import pybullet as p


class Button:
    def __init__(self, buttonId: int):
        self.id = buttonId
        self.counter = 0

    def wasClicked(self) -> bool:
        return p.readUserDebugParameter(self.id) > self.counter

    def consumeClick(self):
        self.counter = p.readUserDebugParameter(self.id)
