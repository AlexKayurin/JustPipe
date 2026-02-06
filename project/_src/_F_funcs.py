# -*- coding: utf-8 -*-

import math
import numpy as np


def Rotation2D(dx, east, north, hdg):
    e_rot = east + dx * math.sin(math.radians(90 + hdg))
    n_rot = north + dx * math.cos(math.radians(90 + hdg))
    return e_rot, n_rot

def Bearing(de, dn):
    # de, dn as np arrays or lists
    grbrg = np.zeros((len(de), 3))
    grbrg[:, 0] = de
    grbrg[:, 1] = dn

    # N
    grbrg[:, 2][(grbrg[:, 0] == 0) & (grbrg[:, 1] >= 0)] = 0
    # S
    grbrg[:, 2][(grbrg[:, 0] == 0) & (grbrg[:, 1] < 0)] = math.radians(180)
    # E
    grbrg[:, 2][(grbrg[:, 0] > 0) & (grbrg[:, 1] == 0)] = math.radians(90)
    # W
    grbrg[:, 2][(grbrg[:, 0] < 0) & (grbrg[:, 1] == 0)] = math.radians(270)
    # NE
    grbrg[:, 2][(grbrg[:, 0] >= 0) & (grbrg[:, 1] > 0)] =\
        np.arctan(grbrg[:, 0][(grbrg[:, 0] >= 0) & (grbrg[:, 1] > 0)] / grbrg[:, 1][(grbrg[:, 0] >= 0) & (grbrg[:, 1] > 0)])
    # SE & SW
    grbrg[:, 2][(grbrg[:, 0] >= 0) & (grbrg[:, 1] < 0)] =\
        np.arctan(grbrg[:, 0][(grbrg[:, 0] >= 0) & (grbrg[:, 1] < 0)] / grbrg[:, 1][(grbrg[:, 0] >= 0) & (grbrg[:, 1] < 0)]) + math.radians(180)

    grbrg[:, 2][(grbrg[:, 0] < 0) & (grbrg[:, 1] < 0)] =\
        np.arctan(grbrg[:, 0][(grbrg[:, 0] < 0) & (grbrg[:, 1] < 0)] / grbrg[:, 1][(grbrg[:, 0] < 0) & (grbrg[:, 1] < 0)]) + math.radians(180)
    # NW
    grbrg[:, 2][(grbrg[:, 0] < 0) & (grbrg[:, 1] > 0)] =\
        np.arctan(grbrg[:, 0][(grbrg[:, 0] < 0) & (grbrg[:, 1] > 0)] / grbrg[:, 1][(grbrg[:, 0] < 0) & (grbrg[:, 1] > 0)]) + math.radians(360)

    return grbrg[:, 2]