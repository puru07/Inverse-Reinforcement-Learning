#!/usr/bin/env python
"""
The main trainer, gets the data, gets features and then trains
to get the weights
"""
__author__ = "Puru Rastogi"
__email__ = "pururastogi@gmail.com"

import numpy as np
import sys
import irl.maxent as maxent
import irl.mdp.gameworld as gameworld
import commons.parser as parser


def trainer(grid_size, gameplay, ndata, traj_len):
    ''' The main trainer, gets the data, gets features and then trains
    to get the weights '''

    # trajectory_length = traj_len    # length of one traj
    discount = 0.1                  # discount past
    # n_trajectories = ndata          # number of traj
    epochs = 50                     # iteration times
    learning_rate = 0.1             # learning rate
    n_actions = 5                   # number of actions

    # transition probability
    transition_probability = parser.defineProb(grid_size, n_actions)

    # definig the game world
    # arena_st = gameplay[0][0]
    arena_st = gameplay[0][0]
    gw = gameworld.Gameworld(grid_size, arena_st, discount)

    # feature matrix dless type
    feature_matrix = gw.feature_matrix(arena_st, "dless")
    print "the points are at ", arena_st.point
    trajectories = parser.getTrajfromGameplay(gameplay, grid_size)

    print "number of traj", len(trajectories[0])
    print "\n total number of states", len(trajectories[0][0])
    print "\n shape of traj data structure ", np.array(trajectories).shape
    r, alpha = maxent.irl(feature_matrix, n_actions, discount,
        np.array(transition_probability), np.array(trajectories),
        epochs, learning_rate)

    return (r.reshape((grid_size, grid_size)), alpha)


def main(startnum=0, endnum=0, namestr='./data/aidata'):
    gameplay, grid_size = parser.getTraj(startnum, endnum, namestr)
    # grid_size = arena_st.grid_size
    traj_len = len(gameplay[0])
    print "got the traj"
    rmap, alpha = trainer(grid_size, gameplay, endnum - startnum +1, traj_len)
    print "the weights are "
    print alpha
    np.save('rmap', rmap)
    np.save('weights', alpha)


if __name__ == '__main__':
    if (len(sys.argv) < 3):
        print "training by default parameters"
        main()
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
