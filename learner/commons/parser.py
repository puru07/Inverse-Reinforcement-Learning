"""
Developer: Zewen Wang
Train the aimlplatform data set using irl
Date: 3/24/2017
"""
import numpy as np
import matplotlib.pyplot as plt

import irl.maxent as maxent

from irl.mdp.gamestate import gamestate as gstate 
from irl.mdp.gamestate import arenastate as astate 

def xy2abs(xy, grid_size):
	return xy[0] + xy[1] * grid_size

def abs2xy(a, grid_size):
	return [a % grid_size, a // grid_size]

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

def singleProb(i, j, k, grid_size):
	"""
	i: State int.
	j: Action int.
	k: State int.
	"""
	xi, yi = abs2xy(i, grid_size)
	xk, yk = abs2xy(k, grid_size)
	if xi - xk == 1 and yi == yk and j == 2:
		return 1
	if xi == xk and yi - yk == 1 and j == 1:
		return 1
	if xi - xk == -1 and yi == yk and j == 0:
		return 1
	if xi == xk and yi - yk == -1 and j == 3:
		return 1
	if xi == xk and yi == yk  and j == 4:
		return 1
	return 0

def defineProb(grid_size, n_actions):
	n_states = grid_size * grid_size

	"""p(s_k | s_i, a_j)"""
	
	res = [[[singleProb(i, j, k, grid_size) \
	for k in range(n_states)] \
	for j in range(n_actions)] \
	for i in range(n_states)]
	return res

def getTraj(path, name, number):

    filename =  path + name + str(number) + ".txt"
    print "parsing file: " + filename
    
    with open(filename) as file:
        line = file.readline().strip()
        wid, hei = line.split(" ")
        wid = int(wid)
        hei = int(hei)
        obs_tup = []
        line = f.readline().strip()
        parts = line.split(" ")
        for i in range(len(parts) / 2):
            obs_tup.append((int(parts[2 * i]), int(parts[2 * i + 1])))
        
        # the states of the game play
        state_tup = ();
        while f.readline() != "":
            f.readline()
            line = f.readline()
            parts = line.strip().split(" ")
            player = (int(parts[1]), int(parts[2]))
            line = f.readline()
            # Ghosts
            parts = line.strip().split(" ")
            nghost = int(parts[1])
            ghost_tup = ()*nghost
            for i in range(nghost):
                line = f.readline()
                parts = line.strip().split(" ")
                ghost_tup[i] = (int(parts[0]), int(parts[1]))
            
            # Points
            line = f.readline()
            parts = line.strip().split(" ")
            npoint = int(parts[1])
            point_tup = ()*npoint
            for i in range(npoint):
                line = f.readline()
                parts = line.strip().split(" ")
                if int(parts[0]) == 0:
                    point_tup[i] = (-1, -1)
                else:
                    point_tup[i] = (int(parts[1]), int(parts[2]))
            state_tup = state_tup + (gstate(player,ghost_tup,point_tup),)
            f.readline()
        f.close()
        arena_st = astate(nghost, npoint,obs_tup)
        return (arena_st,state_tup)

def getMap(address):
	"""the target map matrix"""
	f = open(address)
	line = f.readline()
	grid_size = int(line[0:line.find(" ")])
	n_states = grid_size * grid_size

	ground_r = []

	line = f.readline()
	row = 0
	col = 0
	obs = ()
	point = ()
	while line:
		for s in line:
			if s == '1':
				ground_r.append(1)
				obs = obs + ((col,row),)	
				col = col+1			
			elif s == 'm':
				ground_r.append(0.5)
				point = point + ((col,row),)
				col = col+1
			elif s == '\n':
				col = col+1
				continue
			else:
				col = col+1
				ground_r.append(0)
		col = 0
		row  = row +1
		line = f.readline()
	f.close()
	arena = astate(0,len(point), obs)
	gr_array = np.array(ground_r).reshape((grid_size, grid_size))
	return (arena, grid_size)

def getTraj_old(startfileNum, fileNum, mapId):

	# getting the arena information
	arena_st, grid_size= getMap("./data/aimap4.txt")

	"""trajectory matrix stored in the file"""
	trajectories = []
	state_tup = ()
	for fi in range(startfileNum, fileNum + 1):
		fname = "./data/aidata" + str(fi) + ".txt"
		f = open(fname)
		line = f.readline()	# grid_size
		tralen = 0
		# ftraj = []
		npoint = 0
		point_pos = ()

		while line:
			line = f.readline()		# step number
			line = f.readline()		# position of the player --- line
			# ----------------
			print line[3], line[5]
			player = ( int(line[3]), int(line[5]))	# position of player
			tralen = tralen + 1
			# ----------------
			line = f.readline()			# number of ghost
			line = f.readline()			# number of coins ---- line
			if npoint == 0:
				npoint = int(line[3])
			point_pos = ()			# number of coins
			for point in range(npoint):
				line = f.readline()
				parts = line.strip().split(" ")
				if int(parts[0]) ==0 :
					point_pos = point_pos + ((-1,-1),)
				else:
					point_pos = point_pos + ((int(parts[1]), int(parts[2])),)

			line = f.readline()
			line = f.readline()
			state_tup = state_tup + (gstate(player,(),point_pos),)

		f.close()
		# adding the final position (at the final point) to the trajectory
		for point in point_pos:

			if point[0] == -1 :
				continue
			else:
				player  = (point[0], point[1])
				point = (-1,-1)
				break

		state_tup = state_tup + (gstate(player,(),point_pos),)
		print "Trajectory length: " + str(tralen)

		# for i in range(0, tralen):
		# 	ftraj.append([xy2abs(ppos[i]),\
		# 	getAction(ppos[i], ppos[i+1]), 0])
		
		trajectories.append(state_tup)
		print "Parsed file: " + fname
		#print np.array(trajectories)

	return (arena_st, trajectories, grid_size)

def getTrajfromGameplay(state_tup, grid_size):
	trajectories = []
	trace = []
	for trial_num in range(0,len(state_tup)):
		trace[:] = []
		for state_num in range(0,len(state_tup[trial_num])-1):
			trace.append([xy2abs(state_tup[trial_num][state_num].player, grid_size),\
			getAction(state_tup[trial_num][state_num].player, state_tup[trial_num][state_num+1].player),0])
		state_num = len(state_tup[trial_num])-1
		trace.append([xy2abs(state_tup[trial_num][state_num].player, grid_size),4,0])
		trajectories.append(trace)

	return trajectories		



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