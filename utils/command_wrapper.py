
# This is just a helper class to make debugging easier.
class CommandWrapper:
    def get_dynamics_info(command_result):
        ret = dict()
        ret["mass"] = command_result[0]
        ret["lateral_friction"] = command_result[1]
        ret["local_inertia_diagonal"] = command_result[2]
        ret["local-inertial_pos"] = command_result[3]
        ret["local_inertia_orn"] = command_result[4]
        ret["restitution"] = command_result[5]
        ret["rolling_friction"] = command_result[6]
        ret["spinning_friction"] = command_result[7]
        ret["contact_damping"] = command_result[8]
        ret["contact_stiffness"] = command_result[9]
        ret["body_type"] = command_result[10]
        ret["collision_margin"] = command_result[11]
        return ret
