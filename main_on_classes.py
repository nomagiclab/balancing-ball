#!/usr/bin/env python3
from paddle.only_paddle import OnlyPaddle

import pybullet as p
import pybullet_data
import time

# start the simulation with a GUI (p.DIRECT is without GUI)
p.connect(p.GUI)

# Create a ball.
ball_radius = 0.025
ball_coll = p.createCollisionShape(p.GEOM_SPHERE, radius=ball_radius)
ball = p.createMultiBody(baseMass=0.01,
                         baseCollisionShapeIndex=ball_coll,
                         basePosition=[0.15, 0, 1],
                         baseOrientation=[0, 0, 0, 1])

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

# add controllers to GUI
paddle.create_joint_controllers()

# add rotation speed controller
rotation_speed_id = p.addUserDebugParameter("rotation_speed", 0, 45, 5)

reset_ball_button = p.addUserDebugParameter("Reset ball position", 1, 0, 0)

p.changeDynamics(ball, -1, rollingFriction=0.005, restitution=0.6)

p.stepSimulation()

x_steering = 0
y_steering = 0
reset_ball_val = 0

while True:
    # set joint parameters (we can control position, velocity, acceleration, force, and other)
    paddle.read_and_update_joint_position()

    # add keyboard steering
    keys = p.getKeyboardEvents()

    # get rotation joints positions.
    x_joint_pos = p.getJointState(paddle.robot_id, paddle.rotate_axis_joints['x'])[0]
    y_joint_pos = p.getJointState(paddle.robot_id, paddle.rotate_axis_joints['y'])[0]

    # handle keyboard events
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

    rotation_speed = p.readUserDebugParameter(rotation_speed_id)

    if p.readUserDebugParameter(reset_ball_button) > reset_ball_val:
        reset_ball_val = p.readUserDebugParameter(reset_ball_button)
        p.resetBasePositionAndOrientation(ball, [0.15, 0, 1], [0, 0, 0, 1])

    # Rotate the paddle around the x-axis
    if x_steering != 0:
        paddle.rotate_around_axis('x', x_steering * rotation_speed)

    # Rotate the paddle around the y-axis
    if y_steering != 0:
        paddle.rotate_around_axis('y', y_steering * rotation_speed)

    # step Simulation
    p.stepSimulation()

    time.sleep(0.01)  # sometimes pybullet crashes, this line helps a lot
