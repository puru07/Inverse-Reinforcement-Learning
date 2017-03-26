import math

class node:

	# default values of the parameters
	door_r = 1 			# radiusof the door
	arm_r = 1 			# radius of arm's workspace
	# dimensions of robo
	Width = 0.4  	# along the x
	Len = 0.4 		# along the y

	# dimensions of the arena
	arena_W = 2.4		# along x
	arena_L = 2.4
	dx = Width/4
	dy = Len/4


	def __init__(self,x,y,gcost,parentkey):
		self.x = x
		self.y = y
		self.parentkey = parentkey 
		self.gcost = gcost
		#self.hcost = self.getHcost()

	def getSuccs(self):

		if (self.h == 1 and self.v == 1 and self.d == 1):
			vnew = 0
			tempNode = node(self.x,self.y,self.theta,self.d,self.h,vnew,\
					self.gcost,self.gethashKey())
			action = 5
			tempNode.gcost += tempNode.getTCost(action)
			return [tempNode]

		#list to be returned
		succs = []
		#transition from arm to base and outside to inside
		# (d,h,v) = (1,0,0) -> (1,1,1)
		if (self.h == 0 and self.d == 1 and self.v == 0):
			if math.hypot(self.x,self.y) > node.door_r - node.arm_r/2:
				hnew = 1
				vnew = 1
				tempNode = node(self.x,self.y,self.theta,self.d,hnew,vnew,\
					self.gcost,self.gethashKey())
				action1 = 4
				action2 = 5
				tempNode.gcost += tempNode.getTCost(action1) #+ tempNode.getTCost(action2)
				if tempNode.stateIsvalid():
					succs += [tempNode]
		
		# transition in base footprint
		dx = node.dx
		dy = node.dy
		dtheta = 10

		Posx = []
		Posx += [[self.x + dx,self.y,self.theta]]
		Posx += [[self.x - dx,self.y,self.theta]]

		Posy = []
		#Posy = Posx
		Posy += [[self.x,self.y + dy,self.theta]]
		Posy += [[self.x ,self.y - dy,self.theta]]
		PosT = []
		# creating the nodes and cost of nodes depending on door interval
		succs = []

		for item in Posx:
			succs += self.variants(item, 0)
		for item in Posy:
			succs += self.variants(item, 1)
		# can do the same for change in theta
		
		# shifting between v values and h vales
		tempNode = self
		if self.d == 1:
			# transfering from to base to arm
			if self.h == 0 and self.v == 0:
				tempNode.h = 1
				tempNode.v = 1
				action = 5
				tempNode.gcost += tempNode.getTCost(action)
				if tempNode.stateIsvalid():
					succs += [tempNode]
				else: 
					print 'failure'
				
			# transfering from base to arm
			elif self.h == 1 and self.v ==1:
				tempNode.v = 0
				action = 5
				tempNode.gcost += tempNode.getTCost(action)
				if tempNode.stateIsvalid():
					succs += [tempNode]
				else:
					print 'failure'

		return succs

	def getHcost(self):
		rlen =  node.door_r
		posR = math.hypot(self.x, self.y)
		cost1 = max(0 , posR - rlen)
		
		angleRange = self.getFeasibleAngle()
		angleRange = math.fabs(angleRange[1]) - math.fabs(angleRange[0])
		angleRem = 1.57 - angleRange
		cost2 = 0.1*angleRem
		
		return cost1 + cost2

	def gethashKey(self):
		haskey = self.x*10 + self.y
		return int(haskey)

	def getTCost(self, action):		# Cost of the transition
		cost = 0
		# 0: x , 1: y, 2:theta 3:d, 4:h, 5:v
		if action ==0:
			cost += 3
		elif action == 1:
			cost += 1
		elif action == 2:
			cost += 1
		elif action == 3:
			cost += 3
		elif action == 4:
			cost += 1
		elif action == 5:
			cost += 1

		return cost

	def stateIsvalid(self):
		#checking for arena constraints
		if (self.x < -1*node.door_r and self.y + node.Len/2 >0):
			# print 'barging into the wall', self.x, self.y
			return False
		if (self.x + node.Width/2 > 0 or self.x - node.Width/2 < -1*node.arena_W):
			# print 'barging into the wall', self.x, self.y
			return False
		elif self.y - node.Len/2 < -1*node.arena_L:
			# print 'barging into the wall', self.x, self.y
			return False

		elif self.d == 2:
			if math.hypot(self.x, self.y) > (node.door_r + node.arm_r) :
				# if it is beyond the reach of the arm
				return False
		# checking if it goes through with arm still holding the knob
		if self.d == 1 and self.h == 0:
			if self.y + node.Len/2 >= 0:
				return False

		##########################
		elif self.d == 0:
			# if it is in closed interval
			# if it barging into the door
			if self.y +node.Len/2 >= 0 :
				return False
			angle = self.getFeasibleAngle()
			angle = angle[1]

			#kinematic constraints
			# checking the distance from knob
			if math.hypot(self.x + node.door_r*math.cos(angle), \
							self.y + node.door_r*math.sin(angle)) < node.arm_r:
				# too far from door knob
				return False
		elif self.d == 1:
			# if the door is on open interval
			angle = self.getFeasibleAngle()
			angle = angle[0]
			# if the door is being held from outside
			if self.h == 0:
				if math.hypot(self.x + node.door_r*math.cos(angle), \
							self.y + node.door_r*math.sin(angle)) <  node.arm_r/2 :
					return True
			# if the door is being held from inside
			# elif self.h == 1 :
			# 	if math.hypot(self.x + node.door_r*math.cos(angle), \
			# 				self.y + node.door_r*math.sin(angle)) < node.arm_r :
			# 		return False
		return True

def getSatefromKey(key):
	x = key//10
	y = (key-x*10)

	return [x,y]

def getCost(Node, Weight):
	return (Weight*Node.getHcost() + Node.gcost)
def printNode(Node):
	if Node.d == 0:
		dstring = 'door in close intv '
	elif Node.d == 1:
		dstring = 'door in open intv '
	else:
		dstring = 'fully open door '
	if Node.h ==0:
		hstring = 'holding outside'
	else :
		hstring = 'holding inside'
	if Node.v == 0:
		vstring = 'using Arm'
	else:
		vstring = 'using base'
	print Node.x, Node.y, dstring, hstring, vstring
	print Node.hcost
	#print Node.gethashKey()

	return 0
