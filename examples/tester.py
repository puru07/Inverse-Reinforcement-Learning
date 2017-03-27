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



grid_size = 7
traj_len = 10
traj = parser.getTraj(0,16)
rmap = trainer.trainer(grid_size,traj,17)
astar.init([grid_size,grid_size])
out = astar.astar([0,0],rmap,traj_len)

# getting the tree out
print "figuring out the tree"
node_list = out[1]
currNode = out[0]
tree = []
tree += [currNode]

while True:
	pkey = currNode.parentkey
	if pkey == 0:
		print "tree finished"
		break
	newnode = node_list[pkey]
	tree += [newnode]
	#astar.printNode(newnode)
	currNode = newnode
print 'size of the path is'
print len(tree)


