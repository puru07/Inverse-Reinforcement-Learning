#!/usr/bin/python
"""
Developer: Puru Rastogi
Test the accuracy of path prediction
Date: 3/26/2017
"""

import numpy as np
import irl.maxent as maxent
import irl.mdp.gameworld as gameworld

import commons.parser as parser



def trainer(grid_size,gameplay, ndata):
	discount = 0.1        				# discount past
	epochs = 50                    # iteration times
	learning_rate = 0.1            # learning rate
	n_actions = 5                  # number of actions

    mode = "velnoghost"
	# transition probability
	transition_probability = parser.defineProb(grid_size, n_actions,mode)

	# definig the game world
	arena_st = gameplay[0][0]
	gw = gameworld.Gameworld(grid_size, arena_st,discount)

	# feature matrix dless type
	feature_matrix = gw.feature_matrix(arena_st,"dless",mode)
	trajectories = parser.getTrajfromGameplay(gameplay, grid_size)

	# feature_matrix = []
	# for i in range(0, grid_size * grid_size):
	# 	fmtemp = []
	# 	for j in range(0, grid_size * grid_size):
	# 		if j == i:
	# 			fmtemp.append(1)
	# 		else:
	# 			fmtemp.append(0)
	# 	feature_matrix.append(fmtemp)
	
	#print np.array(feature_matrix)

	"""obtain the learning result"""

	print "number of traj", len(trajectories[0]), \
	"\n total number of states",len(trajectories[0][0]), \
	"\n shape of traj data structure ",np.array(trajectories).shape
	r,alpha = maxent.irl(feature_matrix, n_actions, discount, \
	np.array(transition_probability), np.array(trajectories), epochs, learning_rate)

	return (r.reshape((grid_size, grid_size)), alpha)

	

