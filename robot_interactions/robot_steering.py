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

    def set_tcp(self, positions):
        self.rtde_c.setTcp(positions)

    def move_joints_to_position(self, joint_position, speed=1.05, acceleration=1.4):
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

    def servoJ(
        self,
        positions,
        speed=0.0,
        acceleration=0.0,
        time=0.03,
        lookahead_t=0.05,
        gain=500,
    ):
        self.rtde_c.servoJ(positions, speed, acceleration, time, lookahead_t, gain)

    def move_tool_sync(
        self,
        tool_position,
        speed=0.25,
        acceleration=1.2,
    ):
        self.rtde_c.moveL(tool_position, speed, acceleration)

    def stop(self):
        self.rtde_c.servoStop()
        self.rtde_c.stopJ(2)

    def get_joint_position(self):
        return self.rtde_r.getActualQ()
