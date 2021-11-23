import pybullet as p
import time
import pybullet_data
from utils.button import Button
from utils.command_wrapper import CommandWrapper

# Maybe we should find a way to aggregate those constants.
DEFAULT_BALL_HEIGHT = 1
MAX_BALL_HEIGHT = 2
G = 9.81

if __name__ == "__main__":
    physicsClient = p.connect(p.GUI)
    p.setGravity(0, 0, -G)

    p.setAdditionalSearchPath(pybullet_data.getDataPath())

    plane = p.loadURDF("plane.urdf")

    # TODO Find exact values of this coefficients.
    p.changeDynamics(plane, -1, restitution = 0.4, contactDamping = 10, contactStiffness = 200000)

    DEFAULT_ORIENTATION = p.getQuaternionFromEuler([0, 0, 0])
    ballId = p.loadURDF("urdf_models/ball.urdf", [0, 0, DEFAULT_BALL_HEIGHT])

    # TODO Find exact values of this coefficients.
    # Perhaps constants should be aggregated in a better way.
    # Some of them are in the urdf file, some are passed in the function below. It might be confusing.
    p.changeDynamics(ballId, -1, restitution=1, lateralFriction=0.2, spinningFriction=0.2, rollingFriction=0.2)

    setBallInitHeight = p.addUserDebugParameter("Set initial ball height", 0, MAX_BALL_HEIGHT, DEFAULT_BALL_HEIGHT)
    resetBallButton = Button(p.addUserDebugParameter("Reset ball position", 1, 0, 0))

    while True:
        p.stepSimulation()
        print(CommandWrapper.getDynamicsInfo(p.getDynamicsInfo(ballId, -1)))
        if resetBallButton.wasClicked():
            print("Reset ball position button clicked!")
            height = p.readUserDebugParameter(setBallInitHeight)
            # Also sets velocity to 0.
            p.resetBasePositionAndOrientation(ballId, [0, 0, height], DEFAULT_ORIENTATION)

        time.sleep(0.01)



