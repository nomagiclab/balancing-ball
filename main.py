import pybullet as p
import time
import pybullet_data
from utils.button import Button


physicsClient = p.connect(p.GUI)
p.setGravity(0, 0, -10)

p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.loadURDF("plane.urdf")

startOrientation = p.getQuaternionFromEuler([0,0,0])
startPos = [0, 0, 1]
ballId = p.loadURDF("urdf_models/ball.urdf", startPos, startOrientation)

setBallInitHeight = p.addUserDebugParameter("Set initial ball height", 0, 2, 1)

resetBallButton = Button(p.addUserDebugParameter("Reset ball position", 1, 0, 0))


while True:
    p.stepSimulation()

    if resetBallButton.wasClicked():
        resetBallButton.consumeClick()
        height = p.readUserDebugParameter(setBallInitHeight)
        p.resetBasePositionAndOrientation(ballId, [0, 0, height], [0, 0, 0, 1])

    time.sleep(0.01)



