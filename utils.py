import pybullet_data
from paddle.only_paddle import OnlyPaddle


def load_assets_only_paddle(p):
    BALL_RADIUS = 0.025

    # Create a ball.
    ball_coll = p.createCollisionShape(p.GEOM_SPHERE, radius=BALL_RADIUS)
    ball = p.createMultiBody(baseMass=0.01,
                             baseCollisionShapeIndex=ball_coll,
                             basePosition=[0.15, 0, 1],
                             baseOrientation=[0, 0, 0, 1])

    p.changeDynamics(ball, -1, rollingFriction=0.005, restitution=0.7)

    # we can load plane and cube from pybullet_data
    p.setAdditionalSearchPath(pybullet_data.getDataPath())

    # load a plane (Not the flying one!)
    p.loadURDF("plane.urdf", [0, 0, -0.1], useFixedBase=True)

    # setup gravity (without it there is no gravity at all)
    p.setGravity(0, 0, -10)

    # load our paddle
    paddle = OnlyPaddle(p)

    # display info about robot joints
    numJoints = p.getNumJoints(paddle.robot_id)

    for joint in range(numJoints):
        print(p.getJointInfo(paddle.robot_id, joint))

    return [ball, paddle]

def throw_ball(p, ball, paddle, ball_velocity):
    # Get the padddle's center position.
    paddle_pos = paddle.get_center_position()

    # Throw the ball.