"""
Developer: Puru Rastogi
Test the accuracy of path prediction
Date: 3/26/2017
"""

import numpy as np
import matplotlib.pyplot as plt

import irl.maxent as maxent
import irl.mdp.gameworld as gameworld

import parser 


def trainer(grid_size, trajectories, ndata, traj_len):
	trajectory_length = traj_len   		#length of one traj
	discount = 0.1        				#discount past
	n_trajectories = ndata 		    	#number of traj
	epochs = 200           			#iteration times
	learning_rate = 0.1    				#learning rate
	n_actions = 5;         				#number of actions

	"""transition probability"""
	transition_probability = parser.defineProb(grid_size, n_actions)

	"""feature matrix ident type"""
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
	r = maxent.irl(np.array(feature_matrix), n_actions, discount, \
	np.array(transition_probability), np.array(trajectories), epochs, learning_rate)

	return r.reshape((grid_size, grid_size))