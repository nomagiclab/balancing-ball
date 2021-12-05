import pybullet as p
from typing import List

class Ball:
    DEFAULT_ORIENTATION = [0, 0, 0, 1]
    DEFAULT_BALL_POSITION = [0.15, 0, 1]
    MAX_BALL_HEIGHT = 2

    # https://www.quintic.com/education/case_studies/coefficient_restitution.htm
    RESTITUTION_COEFFICIENT = 0.9

    # http: // isjos.org / JoS / vol7iss1 / Papers / JoSV7p3 - BallSpin.pdf
    FRICTION_COEFFICIENT = 0.2
    def __init__(self, urdf_path: str, startPosition: List[float] =  [0, 0, 1], startOrientation: List[float] = [0, 0, 0, 1]):
        self.id = p.loadURDF("urdf_models/ball.urdf", startPosition, startOrientation)

    def reset