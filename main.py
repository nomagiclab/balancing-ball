#!/usr/bin/env python3

import pybullet as p
import pybullet_data
import time

# start the simulation with a GUI (p.DIRECT is without GUI)
p.connect(p.GUI)

# we can load plane and cube from pybullet_data
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# load a plane (Not the flying one!)
p.loadURDF("plane.urdf", [0, 0, -0.1], useFixedBase=True)

# setup gravity (without it there is no gravity at all)
p.setGravity(0, 0, -10)

# load our paddle definition
robot = p.loadURDF("paddle.urdf")

# load a ball
ball_1 = p.loadURDF("sphere_small.urdf", [0.15, 0, 1], globalScaling=1)

# display info about robot joints
numJoints = p.getNumJoints(robot)
for joint in range(numJoints):
    print(p.getJointInfo(robot, joint))

# add four sliders to GUI
p0_id = p.addUserDebugParameter("z", 0, 3, 0.5)
p1_id = p.addUserDebugParameter("y", -1, 1, 0)
p2_id = p.addUserDebugParameter("x", -1, 1, 0)
p3_id = p.addUserDebugParameter("z_roll", -3.14, 3.14, 0)
p4_id = p.addUserDebugParameter("y_roll", -3.14, 3.14, 0)
p5_id = p.addUserDebugParameter("z_roll", -3.14, 3.14, 0)

p.stepSimulation()

while True:
    # set joint parameters (we can control position, velocity, acceleration, force, and other)
    p.setJointMotorControl2(robot, 0, p.POSITION_CONTROL, p.readUserDebugParameter(p0_id))
    p.setJointMotorControl2(robot, 1, p.POSITION_CONTROL, p.readUserDebugParameter(p1_id))
    p.setJointMotorControl2(robot, 2, p.POSITION_CONTROL, p.readUserDebugParameter(p2_id))
    p.setJointMotorControl2(robot, 3, p.POSITION_CONTROL, p.readUserDebugParameter(p3_id))
    p.setJointMotorControl2(robot, 4, p.POSITION_CONTROL, p.readUserDebugParameter(p4_id))
    p.setJointMotorControl2(robot, 5, p.POSITION_CONTROL, p.readUserDebugParameter(p5_id))

    # step Simulation
    p.stepSimulation()

    time.sleep(0.01)  # sometimes pybullet crashes, this line helps a lot
