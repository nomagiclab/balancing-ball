from pid.pid_balancer import OUT_OF_RANGE, PIDBalancer
from paddle.abc_paddle import ABCPaddle
from trackers.abstract_tracker import AbstractBallTracker
from utils.environment import init_standard_pid_tools
import pybullet


class PidPerformer:
    def __init__(
        self,
        pybullet_client: pybullet,
        ball_tracker: AbstractBallTracker,
        paddle: ABCPaddle,
    ):
        self.pybullet_client = pybullet_client
        self.pid_sliders, self.pid_button, pid_controller = init_standard_pid_tools(
            pybullet_client, 55, -55
        )
        self.pid_balancer = PIDBalancer(ball_tracker, pid_controller)

        self.paddle = paddle
        self.pid_balancer.controller.debug = False

    def perform_pid_step(self):
        desired_angles = self.pid_balancer.calculate_next_angle()

        if desired_angles == OUT_OF_RANGE:
            self.paddle.reset_torque_pos()
        else:
            y_desired_angle, x_desired_angle = desired_angles
            # The y rotation direction is inverted,
            self.paddle.set_angles(x_desired_angle, -y_desired_angle)
            # so we have to take the negative value.

        if self.pid_button.was_clicked():
            self.pid_balancer.change_pid_coefficients(
                self.pybullet_client.readUserDebugParameter(self.pid_sliders["kp"]),
                self.pybullet_client.readUserDebugParameter(self.pid_sliders["ki"]),
                self.pybullet_client.readUserDebugParameter(self.pid_sliders["kd"]),
            )
