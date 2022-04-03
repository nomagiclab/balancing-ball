import math

from trackers.realsense_tracker import RealsenseTracker
from src.vision.realsense import UsbRealsenseCamera, cv2
from pid.pid_balancer import PIDBalancer, OUT_OF_RANGE
from pid.pid_controller import PIDController

tracker = RealsenseTracker(tuple(x / 2 for x in UsbRealsenseCamera.shape()), True)
pid_controller = PIDController(
    float(input("Enter P: ")),
    float(input("Enter I: ")),
    float(input("Enter D: ")),
    25,
    -25,
)

pid_balancer = PIDBalancer(tracker, pid_controller)

while True:
    desired_angles = pid_balancer.calculate_next_angle()

    if desired_angles == OUT_OF_RANGE:
        input("Ball is out of range, press key to continue...")
        continue

    r, p = math.radians(desired_angles[0]), math.radians(desired_angles[1])

    print("ROLL, PITCH =", r, " --- ", p)

    cv2.waitKey(5)
