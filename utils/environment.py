from typing import Tuple, Dict

import pybullet
import pybullet_data

from ball.abc_ball import BALL_RADIUS
from ball.pybullet_ball import PyBulletBall
from ball.pybullet_ball_controller import PyBulletBallController
from pid.pid_controller import PIDController
from paddle.paddle import Paddle
from utils.button import Button

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
    wind_x_controller = p.addUserDebugParameter("Adjust the wind (x axis)", -G, G, 0)
    wind_y_controller = p.addUserDebugParameter("Adjust the wind (y axis)", -G, G, 0)

    return wind_x_controller, wind_y_controller


def init_force_controllers(p):
    force_x_controller = p.addUserDebugParameter("force (x axis)", -1, 1, 0)
    force_y_controller = p.addUserDebugParameter("force (y acis)", -1, 1, 0)
    b = Button(p.addUserDebugParameter("Apply the force", 1, 0, 0))
    return b, force_x_controller, force_y_controller


def apply_force(p: pybullet, ball_id, force_x, force_y):
    p.applyExternalForce(
        ball_id,
        -1,
        [force_x, force_y, 0],
        [BALL_RADIUS, BALL_RADIUS, BALL_RADIUS],
        p.WORLD_FRAME,
    )


def set_wind(p, wind_x_value, wind_y_value):
    p.setGravity(wind_x_value, wind_y_value, -G)


def update_wind_controllers(p, wind_x_controller, wind_y_controller):
    wind_x = p.readUserDebugParameter(wind_x_controller)
    wind_y = p.readUserDebugParameter(wind_y_controller)

    set_wind(p, wind_x, wind_y)


def update_force_controllers(
    p, ball: PyBulletBall, button: Button, force_x_controller, force_y_controller
):
    if button.was_clicked():
        force_x = p.readUserDebugParameter(force_x_controller)
        force_y = p.readUserDebugParameter(force_y_controller)
        apply_force(p, ball.id, force_x, force_y)


def load_plane(p):
    p.setAdditionalSearchPath(pybullet_data.getDataPath())

    # load a plane (Not the flying one!)
    plane = p.loadURDF("plane.urdf", BASE_PLANE_POSITION, useFixedBase=True)
    # TODO Find exact values of this coefficients. Check  contactDamping, contactStiffness.
    p.changeDynamics(
        plane,
        -1,
        restitution=0.7,
        lateralFriction=1,
        contactStiffness=2000,
        contactDamping=10,
    )
    return plane


def load_paddle(p):
    # load our paddle
    paddle = Paddle(p)

    # display info about robot joints
    num_joints = p.getNumJoints(paddle.robot_id)
    for joint in range(num_joints):
        print(p.getJointInfo(paddle.robot_id, joint))

    return paddle


def init_standard_pid_tools(
    p: pybullet,
    max_angle: float,
    min_angle: float,
    default_kp=100,
    default_ki=1,
    default_kd=300,
) -> Tuple[Dict[str, float], Button, PIDController]:
    kp_slider = p.addUserDebugParameter("P", 0, 500, default_kp)
    ki_slider = p.addUserDebugParameter("I", 0, 50, default_ki)
    kd_slider = p.addUserDebugParameter("D", 0, 6000, default_kd)

    set_pid_button = Button(p.addUserDebugParameter("Change PID", 1, 0, 0))

    pid_controller = PIDController(
        p.readUserDebugParameter(kp_slider),
        p.readUserDebugParameter(ki_slider),
        p.readUserDebugParameter(kd_slider),
        max_angle,
        min_angle,
    )

    return (
        {"kp": kp_slider, "ki": ki_slider, "kd": kd_slider},
        set_pid_button,
        pid_controller,
    )


def init_env_and_load_assets(
    p,
) -> Tuple[
    PyBulletBallController,
    PyBulletBall,
    Paddle,
    Tuple[int, int],
    Tuple[Button, int, int],
]:
    init_environment(p)
    wind_controllers = init_wind_controllers(p)
    force_controllers = init_force_controllers(p)

    load_plane(p)
    ball = PyBulletBall(p)
    ball_controller = PyBulletBallController(ball)
    paddle = load_paddle(p)
    return ball_controller, ball, paddle, wind_controllers, force_controllers
