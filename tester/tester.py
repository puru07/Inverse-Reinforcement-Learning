"""
Developer: Puru Rastogi
Test the accuracy of path prediction
Date: 3/26/2017
"""
import support.parser as parser
import support.astar as astar
import support.trainer as trainer
import numpy as np
import matplotlib.pyplot as plt

import irl.maxent as maxent
import irl.mdp.gridworld as gridworld

def print_rmap(rmap):
	print "rmap is "
	for r in  range(grid_size):
		for c in range(grid_size):
			print rmap[r][c],
		print " \n"
	plt.pcolor(rmap)
	plt.colorbar()
	plt.show()
def print_traj(traj):
	for row in traj[0]:
		print parser.abs2xy(row[0])
def getnextstate(astar_out,start):
	# getting the key of the starting node
	snode = astar.node(start[0],start[1],0,0,-1)
	skey = snode.gethashKey();
	# getting the list of nodes out
	nodeList = astar_out[1].values()

	for node in nodeList:
		pkey = node.parentkey
		if pkey == skey:
			
			break
	return node


###############################################################
#============= THE MAIN SCRIPT STARTS ==============
traj_len = 0
try :
	rmap = np.load('rmap.npy')
	print "reward map loaded"
except 	IOError:
	print "no saved reward map found, training....."
	traj, grid_size = parser.getTraj(0,23,5)
	traj_len = len(traj[0])
	print "got the traj"
	rmap = trainer.trainer(grid_size,traj,17, traj_len)
	np.save('rmap',rmap)
	print "training done, rmap extracted, astar started"

#display the map
plt.pcolor(rmap)
plt.colorbar()
plt.title("Recovered reward")
plt.show()


# getting the trrajectory to be tested
tstart = 24
tend = 29
testtraj, grid_size = parser.getTraj(tstart,tend,4)
if traj_len ==0:
	traj_len = len(testtraj[0])
#print_traj(testtraj)

# rounding off and negating the reward map for dijkstra to work on it
rmap = np.round(rmap*(-1),decimals=2)
# print_rmap(rmap)

# intiating dikstra 
astar.init([grid_size,grid_size])

correct = 0
total = 0
for itraj in range(tend - tstart +1) :
	start = parser.abs2xy(testtraj[itraj][0][0])
	for row in testtraj[itraj][1:]:
		next_state = row[0]
		print "true state is ",  parser.abs2xy(next_state)
		out = astar.astar(start,rmap,traj_len)
		pred_node = getnextstate(out,start)
		pred_state = parser.xy2abs([pred_node.x,pred_node.y])
		print "predicted state is ", pred_node.x ,pred_node.y
		total += 1
		if pred_state == next_state:
			correct += 1
		start = parser.abs2xy(next_state)

print "the total number of states tested : ", total 
print "the correct predictions are: ", correct
print "percentage accuracy is ", correct*100/total


