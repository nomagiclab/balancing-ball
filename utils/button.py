import pybullet as p


class Button:
    def __init__(self, button_id: int):
        self.id = button_id
        self.counter = 0

    # returns True if button was clicked since the last time
    # wasClicked returned True.
    def was_clicked(self) -> bool:
        if p.readUserDebugParameter(self.id) > self.counter:
            self.counter = p.readUserDebugParameter(self.id)
            return True
        return False
