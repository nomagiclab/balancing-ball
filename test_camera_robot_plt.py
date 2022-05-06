import math

from plotting.csv_writer import CsvWriter
from trackers.realsense_tracker import RealsenseTracker
from src.vision.realsense import UsbRealsenseCamera, cv2
from pid.pid_balancer import PIDBalancer, OUT_OF_RANGE
from pid.pid_controller import PIDController
from robot_interactions import robot_paddle

IP_ADDRESS = "192.168.1.20"

paddle = robot_paddle.RobotPaddle(IP_ADDRESS)

P = 0.010
I = 0.002
D = 0.020

tracker = RealsenseTracker(tuple(x / 2 for x in UsbRealsenseCamera.shape()), True)
pid_controller = PIDController(P, I, D, 7, -7)

csv_writer_x = CsvWriter("x")
csv_writer_y = CsvWriter("y")

pid_balancer = PIDBalancer(tracker, pid_controller)

print(csv_writer_x.file_name, " ", csv_writer_y.file_name)
input("All set?")

while True:
    desired_angles = pid_balancer.calculate_next_angle(True)

    if desired_angles == OUT_OF_RANGE:
        r, p = 0.0, 0.0
    else:
        r, p = math.radians(desired_angles[0]), math.radians(desired_angles[1])
        csv_writer_x.update([P, I, D, r, pid_balancer.last_err[0] / 100, 0])
        csv_writer_y.update([P, I, D, p, pid_balancer.last_err[1] / 100, 0])

    print("ROLL, PITCH =", r, " --- ", p)

    if abs(r) > 0.2 or abs(p) > 0.2:
        input("PLEASE RECONSIDER!")
        continue

    paddle.set_angles_rp(r, p)
    cv2.waitKey(5)
