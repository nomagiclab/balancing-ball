import pybullet_data
from paddle.paddle import Paddle

G = 9.81
MAX_BALL_HEIGHT = 2
BALL_DEFAULT_ORIENTATION = [0, 0, 0, 1]
BALL_DEFAULT_POSITION = [0.15, 0, 1]
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


# Loads ball urdf and sets dynamics parameters.
def load_ball(p):
    ballId = p.loadURDF("urdf_models/ball.urdf", basePosition=BALL_DEFAULT_POSITION)

    # TODO Find exact values of this coefficients.
    # Perhaps constants should be aggregated in a better way.
    # Some of them are in the urdf file, some are passed in the function below. It might be confusing.
    p.changeDynamics(ballId, -1, restitution=0.7, lateralFriction=0.2, spinningFriction=0.2, rollingFriction=0.002)
    return ballId


def load_paddle(p):
    # load our paddle
    paddle = Paddle(p)

    # display info about robot joints
    numJoints = p.getNumJoints(paddle.robot_id)
    for joint in range(numJoints):
        print(p.getJointInfo(paddle.robot_id, joint))

    return paddle


def init_env_and_load_assets(p):
    init_environment(p)
    wind_controllers = init_wind_controllers(p)
    load_plane(p)
    ball = load_ball(p)
    paddle = load_paddle(p)
    return ball, paddle, wind_controllers
