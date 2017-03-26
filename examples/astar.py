try:
	from Queue import PriorityQueue as pq
except: 
	from queue import PriorityQueue as pq
from Node import node
import Node 

class node:

	# dimensions of the arena
	arena_W = 7		# along x
	arena_L = 7

	def __init__(self,x,y,gcost,parentkey,childnum):
		self.x = x
		self.y = y
		self.parentkey = parentkey 
		self.childnum = childnum +1
		self.gcost = gcost + r_map[x][y]

	def getSuccs(self, r_map):
		x = self.x
		y = self.y
		# list of successors to be returned
		succs = [] 
		if x + 1 < arena_W +1:
			succs += node(x+1,y self.gcost,self.gethashKey(),self.childnum)
		if x-1 >-1 :
			succs += node(x-1,y self.gcost,self.gethashKey(),self.childnum)
		if y + 1 < arena_L +1 :
			succs += node(x,y+1 self.gcost,self.gethashKey(),self.childnum)
		if y-1 > -1:
			succs += node(x,y-1 self.gcost,self.gethashKey(),self.childnum)
		return succs
	def gethashKey(self):
		haskey = self.x*100 + self.y
		return int(haskey)


def getCost(Node, Weight):
	return (Weight*Node.getHcost() + Node.gcost)

def getSatefromKey(key):
	x = key//100
	y = (key-x*100)

	return [x,y]
def init(arena):

	node.arena_W = arena[0]
	node.arena_L = arena[1]

def astar(start,r_map, traj_lim):
	#print 	node.door_r ,node.arm_r , node.Width , node.Len ,node.arena_W , node.arena_L 
	closelist = {}
	openlist = pq()
	openlist_f = {}
	gstart = 0
	parent_start = 0
	childnum = -1
	start_node = node(start[0],start[1],gstart,parent_start,childnum)
	openlist.put((Node.getCost(start_node,weight),start_node))
	openlist_f[start_node.gethashKey()] = start_node

	while (openlist.qsize()>0):
		# print 'size of open list'
		# print openlist.qsize()
		# getting the node to expand 
		LCNode = openlist.get()			# least cost node
		node2exp = LCNode[1]
		# print 'the hcost from different calls'
		# print node2exp.hcost
		# print node2exp.getHcost()
		#print 'the node expand'
		#printNode(node2exp)
		#checking if the node2exp is the goal
		if node2exp.childnum == traj_lim :
			print 'goal reached via hcost'
			Node.printNode(node2exp)
			print node2exp.getFeasibleAngle()
			print 'number of expansions'
			print len(closelist)
			print 'teh cost'
			print Node.getCost(node2exp, weight)	
			return [node2exp,closelist]

		#expanding the node
		succs = node2exp.getSuccs()
		# print 'number of succs'
		# print len(succs)
		for item in succs:
			if item.gethashKey() in closelist:
				# print 'duplicate ', item.gethashKey() , ' is the key'
				continue
			if item.gethashKey() in openlist_f:
				# print 'duplicate in open list'
				continue
			# printNode(item)
			openlist.put((item.gcost,item))
			openlist_f[item.gethashKey()] = item

		# moving the expanded node to close list, and removing from open list dict
		closelist[node2exp.gethashKey()] = node2exp
		#del openlist_f[node2exp.gethashKey()]

	return 0


#  the main function
if __name__ == '__main__':
	import sys
	startx = float(sys.argv[1])
	starty = float(sys.argv[2])
	startTheta = float(sys.argv[3])
	goalx = float(sys.argv[4])
	goaly = float(sys.argv[5])
	goalTheta = float(sys.argv[6])
	w = float(sys.argv[7])
	out =  astar([startx, starty, startTheta], [goalx, goaly, goalTheta], w)
	if out == 0 :
		print 'failure'
	else:
		print 'success'
