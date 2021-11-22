#!/usr/bin/env python3

import pybullet as p
import pybullet_data
import time

# start the simulation with a GUI (p.DIRECT is without GUI)
p.connect(p.GUI)
red_radius = 0.025

red_ball_coll = p.createCollisionShape(p.GEOM_SPHERE, radius=red_radius)

red_ball = p.createMultiBody(baseMass=0.01,
                             baseCollisionShapeIndex=red_ball_coll,
                             basePosition=[0.15, 0, 1],
                             baseOrientation=[0, 0, 0, 1])

# we can load plane and cube from pybullet_data
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# load a plane (Not the flying one!)
p.loadURDF("plane.urdf", [0, 0, -0.1], useFixedBase=True)

# setup gravity (without it there is no gravity at all)
p.setGravity(0, 0, -10)

# load our paddle definition
robot = p.loadURDF("paddle/paddle.urdf")

# load a ball
# ball_1 = p.loadURDF("sphere_small.urdf", [0.15, 0, 1], globalScaling=1)

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
p5_id = p.addUserDebugParameter("x_roll", -3.14, 3.14, 0)

rotation_speed_id = p.addUserDebugParameter("rotation_speed")

p.changeDynamics(robot, 6, lateralFriction=0.05, spinningFriction=0.1, rollingFriction=0.1, restitution=0.95, mass=1)
p.changeDynamics(red_ball, -1, rollingFriction=0.005, restitution=0.6)

p.stepSimulation()

x_steering = 0
y_steering = 0

while True:
    # set joint parameters (we can control position, velocity, acceleration, force, and other)
    p.setJointMotorControl2(robot, 0, p.POSITION_CONTROL, p.readUserDebugParameter(p0_id))
    p.setJointMotorControl2(robot, 1, p.POSITION_CONTROL, p.readUserDebugParameter(p1_id))
    p.setJointMotorControl2(robot, 2, p.POSITION_CONTROL, p.readUserDebugParameter(p2_id))
    p.setJointMotorControl2(robot, 3, p.POSITION_CONTROL, p.readUserDebugParameter(p3_id))
    p.setJointMotorControl2(robot, 4, p.POSITION_CONTROL, p.readUserDebugParameter(p4_id))
    p.setJointMotorControl2(robot, 5, p.POSITION_CONTROL, p.readUserDebugParameter(p5_id))
    keys = p.getKeyboardEvents()

    x_joint_pos = p.getJointState(robot, 5)[0]
    y_joint_pos = p.getJointState(robot, 4)[0]

    for k, v in keys.items():
        if k == p.B3G_RIGHT_ARROW and (v & p.KEY_WAS_TRIGGERED):
            x_steering = -1
        if k == p.B3G_RIGHT_ARROW and (v & p.KEY_WAS_RELEASED):
            x_steering = 0

        if k == p.B3G_LEFT_ARROW and (v & p.KEY_WAS_TRIGGERED):
            x_steering = 1
        if k == p.B3G_LEFT_ARROW and (v & p.KEY_WAS_RELEASED):
            x_steering = 0

        if k == p.B3G_UP_ARROW and (v & p.KEY_WAS_TRIGGERED):
            y_steering = 1
        if k == p.B3G_UP_ARROW and (v & p.KEY_WAS_RELEASED):
            y_steering = 0

        if k == p.B3G_DOWN_ARROW and (v & p.KEY_WAS_TRIGGERED):
            y_steering = -1
        if k == p.B3G_DOWN_ARROW and (v & p.KEY_WAS_RELEASED):
            y_steering = 0

    # Rotate the paddle around the x-axis
    if x_steering != 0:
        p.setJointMotorControl2(robot,
                                5,
                                p.POSITION_CONTROL,
                                targetPosition=x_joint_pos + x_steering * (5 * 3.14 / 180))

    if y_steering != 0:
        p.setJointMotorControl2(robot,
                                4,
                                p.POSITION_CONTROL,
                                targetPosition=y_joint_pos + y_steering * (5 * 3.14 / 180))

    # step Simulation
    p.stepSimulation()

    time.sleep(0.01)  # sometimes pybullet crashes, this line helps a lot
