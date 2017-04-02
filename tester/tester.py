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


astar.init([grid_size,grid_size])

out = astar.astar([0,0],rmap*(-1),traj_len)
print "astar done with 00 as start"
# getting the tree out
print "figuring out the tree"
node_list = out[1]
currNode = out[0]
tree = []
tree += [currNode]
print "rmap is "
for r in  range(grid_size):
	for c in range(grid_size):
		print rmap[r][c]*(-1),
	print " \n"
print "\n the astar tree is"
while True:
	pkey = currNode.parentkey
	if pkey == 0:
		print "tree finished"
		break
	newnode = node_list[pkey]
	tree += [newnode]
	astar.printNode(newnode)
	currNode = newnode
print 'size of the path is'
print len(tree)
plt.pcolor(rmap*(-1))
plt.colorbar()
plt.show()


