"""
Developer: Puru Rastogi
Test the accuracy of path prediction
Date: 3/26/2017
"""
import parser
import astar
import trainer
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
def gettree(astar_out,start):
	# getting the tree out
	snode = astar.node(start[0],start[1],0,0,-1)
	skey = snode.gethashKey();
	node_list = out[1]
	currNode = out[0]
	tree = []
	tree += [currNode]
	# print "\n the astar tree is"
	while True:
		pkey = currNode.parentkey
		if pkey == skey:
			
			break
		newnode = node_list[pkey]
		tree += [newnode]
		# astar.printNode(newnode)
		currNode = newnode

	return tree

grid_size = 7
traj_len = 10
try :
	rmap = np.load('rmap.npy')
	print "reward map loaded, astar started"
except 	IOError:
	print "no saved reward map found, training....."
	traj = parser.getTraj(0,16,4)
	print "got the traj"
	rmap = trainer.trainer(grid_size,traj,17, traj_len)
	np.save('rmap',rmap)
	print "training done, rmap extracted, astar started"

# intiating dikstra 
astar.init([grid_size,grid_size])

# getting the trrajectory to be tested
testtraj = parser.getTraj(17,17,4)
print_traj(testtraj)
# rounding off and negating the reward map for dijkstra to work on it
rmap = np.round(rmap*(-1),decimals=2)

# print_rmap(rmap)
correct = 0
total = 0
start = parser.abs2xy(testtraj[0][0][0])
for row in testtraj[0][1:]:
	next_state = row[0]
	print "true state is ",  parser.abs2xy(next_state)
	out = astar.astar(start,rmap,traj_len)
	tree = gettree(out,start)
	start = parser.abs2xy(next_state)
	pred_state = parser.xy2abs([tree[-1].x,tree[-1].y])
	print "predicted state is ", tree[-1].x ,tree[-1].y
	total += 1
	if pred_state == next_state:
		correct += 1


print "the total number of states tested : ", total 
print "the correct predictions are: ", correct


