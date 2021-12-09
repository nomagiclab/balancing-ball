from ball.abc_ball import ABCBall
from controllers.pid_balancer import OUT_OF_RANGE
from paddle.abc_paddle import ABCPaddle
from utils.environment import init_standard_pid_tools
import pybullet


class PidPerformer:
    def __init__(self, pybullet_client: pybullet, ball: ABCBall, paddle: ABCPaddle):
        self.pybullet_client = pybullet_client
        self.pid_sliders, self.pid_button, self.pid_balancer = init_standard_pid_tools(
            pybullet_client, ball, paddle, 55, -55)
        self.paddle = paddle
        self.pid_balancer.controller.debug_on()

    def perform_pid_step(self):
        desired_angles = self.pid_balancer.calculate_next_angle()

        if desired_angles == OUT_OF_RANGE:
            self.paddle.reset_torque_pos()
        else:
            y_desired_angle, x_desired_angle = self.pid_balancer.calculate_next_angle()
            self.paddle.set_angle_on_axis('x', x_desired_angle)
            # The y rotation direction is inverted,
            # so we have to take the negative value.
            self.paddle.set_angle_on_axis('y', -y_desired_angle)

        if self.pid_button.was_clicked():
            self.pid_balancer.change_pid_coefficients(*[float(self.pybullet_client.readUserDebugParameter(slider_id))
                                                        for _, slider_id in self.pid_sliders.items()])
