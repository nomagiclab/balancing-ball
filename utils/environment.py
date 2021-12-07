from typing import Tuple

import pybullet_data

from ball.pybullet_ball import PybulletBall
from ball.pybullet_ball_controller import PybulletBallController
from paddle.paddle import Paddle

G = 9.81
BASE_PLANE_POSITION = [0, 0, -0.1]


def init_environment(p):
    # start the simulation with a GUI (p.DIRECT is without GUI)
    p.connect(p.GUI)

    # setup gravity (without it there is no gravity at all)
    p.setGravity(0, 0, -G)

    # Here we can setup elements like wind speed etc.
    pass


def init_wind_controllers(p):
    wind_x_controller = p.addUserDebugParameter("Adjust the wind (x - axis)", -G, G, 0)
    wind_y_controller = p.addUserDebugParameter("Adjust the wind (y - axis)", -G, G, 0)

    return wind_x_controller, wind_y_controller


def update_wind_controllers(p, wind_x_controller, wind_y_controller):
    wind_x = p.readUserDebugParameter(wind_x_controller)
    wind_y = p.readUserDebugParameter(wind_y_controller)

    p.setGravity(wind_x, wind_y, -G)


def load_plane(p):
    p.setAdditionalSearchPath(pybullet_data.getDataPath())

    # load a plane (Not the flying one!)
    plane = p.loadURDF("plane.urdf", BASE_PLANE_POSITION, useFixedBase=True)
    # TODO Find exact values of this coefficients. Check  contactDamping, contactStiffness.
    p.changeDynamics(plane, -1, restitution=0.7, contactStiffness=2000, contactDamping=10)
    return plane


def load_paddle(p):
    # load our paddle
    paddle = Paddle(p)

    # display info about robot joints
    num_joints = p.getNumJoints(paddle.robot_id)
    for joint in range(num_joints):
        print(p.getJointInfo(paddle.robot_id, joint))

    return paddle


def init_env_and_load_assets(p) -> Tuple[PybulletBallController, Paddle, Tuple[int, int]]:
    init_environment(p)
    wind_controllers = init_wind_controllers(p)
    load_plane(p)
    ball_controller = PybulletBallController(PybulletBall(p))
    paddle = load_paddle(p)
    return ball_controller, paddle, wind_controllers
