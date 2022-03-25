import math

from trackers.realsense_tracker import RealsenseTracker
from src.vision.realsense import UsbRealsenseCamera
from pid.pid_balancer import PIDBalancer, OUT_OF_RANGE
from pid.pid_controller import PIDController
from robot_interactions import robot_paddle

IP_ADDRESS = "192.168.1.20"

paddle = robot_paddle.RobotPaddle(IP_ADDRESS)

P = 0.010
I = 0.001
D = 0.015

tracker = RealsenseTracker(tuple(x / 2 for x in UsbRealsenseCamera.shape()), True)
pid_controller = PIDController(P, I, D, 7, -7)

pid_balancer = PIDBalancer(tracker, pid_controller)


while True:
    desired_angles = pid_balancer.calculate_next_angle(True)

    if desired_angles == OUT_OF_RANGE:
        r, p = 0., 0.
    else:
        r, p = math.radians(desired_angles[0]), math.radians(desired_angles[1])

    print("ROLL, PITCH =", r, " --- ", p)

    if abs(r) > 0.2 or abs(p) > 0.2:
        input("PLEASE RECONSIDER!")
        continue

    paddle.set_angles_rp(r, p)
