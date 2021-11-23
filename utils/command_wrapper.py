
# This is just a helper class to make debugging easier.
class CommandWrapper:
    def getDynamicsInfo(commandResult):
        ret = dict()
        ret["mass"] = commandResult[0]
        ret["lateral_friction"] = commandResult[1]
        ret["local_inertia_diagonal"] = commandResult[2]
        ret["local-inertial_pos"] = commandResult[3]
        ret["local_inertia_orn"] = commandResult[4]
        ret["restitution"] = commandResult[5]
        ret["rolling_friction"] = commandResult[6]
        ret["spinning_friction"] = commandResult[7]
        ret["contact_damping"] = commandResult[8]
        ret["contact_stiffness"] = commandResult[9]
        ret["body_type"] = commandResult[10]
        ret["collision_margin"] = commandResult[11]
        return ret
