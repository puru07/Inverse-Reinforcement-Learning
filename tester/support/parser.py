"""
Developer: Zewen Wang
Train the aimlplatform data set using irl
Date: 3/24/2017
"""
import numpy as np
import matplotlib.pyplot as plt

import irl.maxent as maxent
import irl.mdp.gridworld as gridworld

def xy2abs(xy):
	return xy[0] + xy[1] * 7

def abs2xy(a):
	return [a % 7, a // 7]

def getAction(cur, next):
	"""0 -> ; 2 <-; 3 down; 1 up"""
	if cur[0] - next[0] == 1:
		return 2
	if cur[1] - next[1] == 1:
		return 1
	if next[0] - cur[0] == 1:
		return 0
	if next[1] - cur[1] == 1:
		return 3
	if next[1] - cur[1] == 0 and next[0] - cur[0] ==0:
		return 4
	return 0

def singleProb(i, j, k):
	"""
	i: State int.
	j: Action int.
	k: State int.
	"""
	xi, yi = abs2xy(i)
	xk, yk = abs2xy(k)
	if xi - xk == 1 and yi == yk and j == 2:
		return 1
	if xi == xk and yi - yk == 1 and j == 1:
		return 1
	if xi - xk == -1 and yi == yk and j == 0:
		return 1
	if xi == xk and yi - yk == -1 and j == 3:
		return 1
	return 0

def defineProb(grid_size, n_actions):
	n_states = grid_size * grid_size

	"""p(s_k | s_i, a_j)"""
	
	res = [[[singleProb(i, j, k) \
	for k in range(n_states)] \
	for j in range(n_actions)] \
	for i in range(n_states)]
	return res

def getTraj(startfileNum, fileNum, mapId):
	"""the target map matrix"""
	f = open("./data/aimap5.txt")
	line = f.readline()
	grid_size = int(line[0:line.find(" ")])
	n_states = grid_size * grid_size
	ground_r = []

	line = f.readline()
	while line:
		for s in line:
			if s == '1':
				ground_r.append(1)
			elif s == 'm':
				ground_r.append(0.5)
			elif s == '\n':
				continue
			else:
				ground_r.append(0)
		line = f.readline()

	f.close();
	gr_array = np.array(ground_r).reshape((grid_size, grid_size))

	"""trajectory matrix stored in the file"""
	trajectories = []
	for fi in range(startfileNum, fileNum + 1):
		fname = "./data/aidata" + str(fi) + ".txt"
		f = open(fname)
		line = f.readline()	# grid_size
		tralen = 0
		ppos = []
		ftraj = []
		ncoins = 0

		while line:
			line = f.readline()		# step number
			line = f.readline()		# position of the player --- line
			# ----------------
			print line[3], line[5]
			ppos.append([int(line[3]), int(line[5])])	# position of player
			tralen = tralen + 1
			# ----------------
			line = f.readline()			# number of ghost
			line = f.readline()			# number of coins ---- line
			if ncoins == 0:
				ncoins = int(line[3])			# number of coins
			for coins in range(ncoins):
				line = f.readline()
			line = f.readline()
			line = f.readline()
		f.close()
		ppos.append([6,0])
		print "Trajectory length: " + str(tralen)

		for i in range(0, tralen):
			ftraj.append([xy2abs(ppos[i]),\
			getAction(ppos[i], ppos[i+1]), 0])
		
		trajectories.append(ftraj)
		print "Parsed file: " + fname
		#print np.array(trajectories)

	return (trajectories, grid_size)


def main(fileNum, mapId):
	# learning parameters 
	trajectory_length = 10  	# length of one traj
	discount = 0.1         		#discount past
	n_trajectories = 21     	#number of traj
	epochs = 200            	#iteration times
	learning_rate = 0.1    		#learning rate
	n_actions = 4;          	#number of actions
	trajectories = getTraj();

	"""transition probability"""
	transition_probability = defineProb(grid_size, n_actions)

	"""feature matrix ident type"""
	feature_matrix = []
	for i in range(0, grid_size * grid_size):
		fmtemp = []
		for j in range(0, grid_size * grid_size):
			if j == i:
				fmtemp.append(1)
			else:
				fmtemp.append(0)
		feature_matrix.append(fmtemp)
	#print np.array(feature_matrix)

	"""obtain the learning result"""
	r = maxent.irl(np.array(feature_matrix), n_actions, discount, \
	np.array(transition_probability), np.array(trajectories), epochs, learning_rate)

	# """plot the result"""
	plt.subplot(1, 2, 1)
	plt.pcolor(gr_array)
	plt.colorbar()
	plt.title("origin map")

	plt.subplot(1, 2, 2)
	plt.pcolor(r.reshape((grid_size, grid_size)))
	plt.colorbar()
	plt.title("learned reward")

	plt.show()

if __name__ == '__main__':
	main(20, 4)