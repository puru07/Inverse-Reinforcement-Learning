#!/usr/bin/env python
""" Test the accuracy of path prediction"""
__author__ = "Puru Rastogi"
__email__ = "pururastogi@gmail.com"

import commons.parser as parser
import commons.astar as astar
import commons.trainer as trainer
from commons.reward import getRewardMap as getRmap
import numpy as np
import matplotlib.pyplot as plt
import os


def print_rmap(rmap):
    print "rmap is "
    for r in range(grid_size):
        for c in range(grid_size):
            print rmap[r][c],
        print " \n"
    plt.pcolor(rmap)
    plt.colorbar()
    plt.show()


def print_traj(traj):
    for row in traj[0]:
        print parser.abs2xy(row[0])


def getnextstate(astar_out, start, grid_size):
    # getting the key of the starting node
    snode = astar.node(start[0], start[1], 0, 0, -1)
    skey = snode.gethashKey(grid_size)
    # getting the list of nodes out
    nodeList = astar_out[1].values()

    for node in nodeList:
        pkey = node.parentkey
        if pkey == skey:

            break
    return node


###############################################################
#  THE MAIN SCRIPT STARTS

# getting the weights
traj_len = 0
try:
    alpha = np.load('weights.npy')
    print "weights loaded"
except IOError:
    print "no saved weights were found, training....."
    gameplay, grid_size = parser.getTraj(0, 30, './data/aidata')
    # grid_size = arena_st.grid_size
    traj_len = len(gameplay[0])
    print "got the traj"
    _, alpha = trainer.trainer(grid_size, gameplay, 31, traj_len)
    print "the weights are "
    print alpha
    np.save('weights', alpha)
    # np.save('rmap', rmap)
    # print "training done, rmap extracted, astar started"
    # # display the map
    # point_tup = gameplay[0][0].point
    # print "the points are at ", point_tup
    # rmap2 = np.copy(rmap)
    # for point in point_tup:
    #     rmap2[point[1]][point[0]] = 0
    #     rmap2[point[1]][point[0]] = np.amax(rmap2)
    # rmap2 = np.flipud(rmap2)

    # plotting
    # plt.pcolor(rmap2)
    # plt.colorbar()
    # plt.title("Recovered reward")
    # plt.show()
    # print "map is plotted!!"

##############################################################
# -----  LET THE TESTING BEGIN !!!

correct = 0
total = 0
traj_len = 10
directory = './test/'

# loop going through each test file
for filename in os.listdir(directory):
    # filename = test_folder + str(fileindx) + '.txt'
    print "testing file ", filename
    [arena_st, traj], grid_size = parser.getOneTraj(directory + filename)

    # getting the reward map
    rmap = getRmap(alpha, arena_st, grid_size)

    # rounding off and negating the reward map for dijkstra to work on it
    rmap = np.round(rmap * (-1), decimals=2)
    # print_rmap(rmap)

    # intiating dikstra
    astar.init([grid_size, grid_size])

    # getting the goal to clip the trajectories
    # figure out the last point pos
    for states in reversed(traj):
        for points in states.point:
            if points[0] != -1:
                last_state = states
                goal_pos = (points[0], points[1])
                break

    start = traj[0]

    # loop to go through each state
    for next_state in traj[1:]:

        print "true state is ", next_state.player
        out = astar.astar(start.player, rmap, traj_len, grid_size)
        pred_node = getnextstate(out, start.player, grid_size)
        print "predicted state is ", pred_node.x, pred_node.y
        total += 1
        if pred_node.x == next_state.player[0] and \
                pred_node.y == next_state.player[1]:
            correct += 1
        if next_state.player[0] == goal_pos[0] and \
                next_state.player[1] == goal_pos[1]:
            break
        start = next_state
        # if next_state == goal_abs:
        #   break

print "the total number of states tested : ", total
print "the correct predictions are: ", correct
print "percentage accuracy is ", correct * 100 / total
