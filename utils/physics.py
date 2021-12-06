import operator


def add_vertices(v1, v2):
    assert len(v1) == len(v2)
    return tuple(map(operator.add, v1, v2))

def sub_vertices(v1, v2):
    assert len(v1) == len(v2)
    return tuple(map(operator.sub, v1, v2))

# Finds recommended force needed to let ball travel some distant.
def scale_vector(v):
    assert len(v) == 3
    return (1.3 * v[0], 1.3 * v[1], v[2] + 2)

# Transforms 2 positions into force vector required to throw the ball.
def get_force_vector(vec1, vec2):
    vec = sub_vertices(vec2, vec1)
    vec = scale_vector(vec)
    return vec
