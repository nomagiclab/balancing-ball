import pybullet_data
from paddle.only_paddle import OnlyPaddle

MAX_BALL_HEIGHT = 2
G = 9.81
DEFAULT_ORIENTATION = [0, 0, 0, 1]
BASE_PLANE_POSITION = [0, 0, -0.1]
DEFAULT_BALL_POSITION = [0.15, 0, 1]


def init_environment(p):
    # start the simulation with a GUI (p.DIRECT is without GUI)
    p.connect(p.GUI)

    # setup gravity (without it there is no gravity at all)
    p.setGravity(0, 0, -G)

    # Here we can setup elements like wind speed etc.
    pass


def load_plane(p):
    p.setAdditionalSearchPath(pybullet_data.getDataPath())

    # load a plane (Not the flying one!)
    plane = p.loadURDF("plane.urdf", BASE_PLANE_POSITION, useFixedBase=True)
    # TODO Find exact values of this coefficients. Check  contactDamping, contactStiffness.
    p.changeDynamics(plane, -1, restitution=0.7, contactStiffness=2000, contactDamping=10)
    return plane


# Loads ball urdf and sets dynamics parameters.
def load_ball(p):
    ballId = p.loadURDF("urdf_models/ball.urdf", basePosition=DEFAULT_BALL_POSITION)

    # TODO Find exact values of this coefficients.
    # Perhaps constants should be aggregated in a better way.
    # Some of them are in the urdf file, some are passed in the function below. It might be confusing.
    p.changeDynamics(ballId, -1, restitution=0.7, lateralFriction=0.2, spinningFriction=0.2, rollingFriction=0.02)
    return ballId


def load_paddle(p):
    # load our paddle
    paddle = OnlyPaddle(p)

    # display info about robot joints
    numJoints = p.getNumJoints(paddle.robot_id)
    for joint in range(numJoints):
        print(p.getJointInfo(paddle.robot_id, joint))

    return paddle


def init_env_and_load_assets(p):
    init_environment(p)
    load_plane(p)
    ball = load_ball(p)
    paddle = load_paddle(p)
    return ball, paddle
