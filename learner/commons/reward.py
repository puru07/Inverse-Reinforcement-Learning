#!/usr/bin/env python
''' calculates the reward map using weights and arena map'''
__author__ = "Puru Rastogi"
__email__ = "pururastogi@gmail.com"

import irl.mdp.gameworld as gameworld
import commons.parser as parser
import sys
import numpy as np
import matplotlib.pyplot as plt


def getRewardMap(alpha, arena_st, grid_size):

    gw = gameworld.Gameworld(grid_size, arena_st)
    feature_matrix = gw.feature_matrix(arena_st, "dless")

    n_states = grid_size * grid_size

    reward_vec = feature_matrix.dot(alpha).reshape((n_states,))
    return reward_vec.reshape((grid_size, grid_size))


def main(alpha_add, map_add, mode=0):
        # mode 0 : for reading from a map file
        # mode 1 : for reading from a map inside a data file
    alpha = np.load(alpha_add)
    if mode == 0:
        arena_st, grid_size = parser.getMap(map_add)
    else:
        arena_st, grid_size = parser.getMap2(map_add)
    rmap = getRewardMap(alpha, arena_st, grid_size)

    # adjusting before plotting
    point_tup = arena_st.point
    rmap2 = np.copy(rmap)
    for point in point_tup:
        rmap2[point[1]][point[0]] = 0
        rmap2[point[1]][point[0]] = np.amax(rmap2)
    rmap2 = np.flipud(rmap2)

    # plotting
    plt.pcolor(rmap2)
    plt.colorbar()
    plt.title("Recovered reward")
    plt.show()


if __name__ == '__main__':
    if (len(sys.argv) < 3):
        print "usage: reward.py path/to/weights.npy path/to/map.txt"
        sys.exit()
    main(sys.argv[1], sys.argv[2], sys.argv[3])
