import rtde_control
import rtde_receive


class Robot:
    FREQUENCY = 500

    def __init__(
        self,
        ip_address,
    ):
        self.time = 1 / self.FREQUENCY

        self.ip_address = ip_address
        self.rtde_c = rtde_control.RTDEControlInterface(
            self.ip_address, rtde_control.RTDEControlInterface.FLAG_USE_EXT_UR_CAP
        )

        self.rtde_r = rtde_receive.RTDEReceiveInterface(self.ip_address)

    def move_joint_to_position(self, joint_position, speed=1.05, acceleration=1.4):
        """speed and acceleration default values are taken
        from moveJ"""
        self.rtde_c.moveJ(joint_position, speed, acceleration)

    def get_tool_position(self):
        return self.rtde_r.getActualTCPPose()

    def move_tool_smooth(
        self,
        tool_position,
        speed=0.5,
        acceleration=0.5,
        lookahead_time=0.1,
        gain=300,
    ):
        # TODO use servoL or servoC?
        # Speed and acceleration are ignored in current version of ur_rtde.
        self.rtde_c.servoL(
            tool_position,
            speed,
            acceleration,
            self.time,
            lookahead_time,
            gain,
        )

    def stop(self):
        self.rtde_c.servoStop()
        self.rtde_c.stopScript()
