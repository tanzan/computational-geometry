import numpy as np


def oriented(from_seg, to_seg):

    a1 = from_seg.angle
    a2 = to_seg.angle
    a = a2 - a1

    if a > np.pi:
        return a - 2 * np.pi
    elif np.abs(a) == np.pi:
        return -a

    return a
