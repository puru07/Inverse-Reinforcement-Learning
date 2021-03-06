#!/usr/bin/env python
'''astar for predicting the path on the
given reward map '''

__author__ = "Puru Rastogi"
__email__ = "pururastogi@gmail.com"


try:
    from Queue import PriorityQueue as pq
except():
    from queue import PriorityQueue as pq

# import numpy as np


class node:

    # dimensions of the arena
    arena_W = 7     # along x
    arena_L = 7

    def __init__(self, x, y, gcost, parentkey, childnum):
        self.x = x
        self.y = y
        self.parentkey = parentkey
        self.childnum = childnum + 1
        self.gcost = gcost

    def getSuccs(self, r_map, grid_size):
        x = self.x
        y = self.y
        # list of successors to be returned
        succs = []
        if x + 1 < node.arena_W:
            succs.append(node(x + 1, y, self.gcost +
                              r_map[y][x + 1], self.gethashKey(grid_size), self.childnum))
        if x - 1 > -1:
            succs.append(node(x - 1, y, self.gcost +
                              r_map[y][x - 1], self.gethashKey(grid_size), self.childnum))
        if y + 1 < node.arena_L:
            succs.append(node(x, y + 1, self.gcost +
                              r_map[y + 1][x], self.gethashKey(grid_size), self.childnum))
        if y - 1 > -1:
            succs.append(node(x, y - 1, self.gcost +
                              r_map[y - 1][x], self.gethashKey(grid_size), self.childnum))
        return succs

    def gethashKey(self, grid_size):
            haskey = self.x * grid_size + self.y
            return int(haskey)


# def getCost(Node, Weight):
#   return (Weight*Node.getHcost() + Node.gcost)

def getSatefromKey(key):
    x = key // 100
    y = (key - x * 100)

    return [x, y]


def init(arena):

    node.arena_W = arena[0]
    node.arena_L = arena[1]


def astar(start, r_map, traj_lim, grid_size):
    # print   node.door_r ,node.arm_r , node.Width , node.Len ,node.arena_W ,
    # node.arena_L
    closelist = {}
    openlist = pq()
    openlist_f = {}
    gstart = 0
    parent_start = -1
    childnum = -1
    start_node = node(start[0], start[1], gstart, parent_start, childnum)
    openlist.put((start_node.gcost, start_node))
    openlist_f[start_node.gethashKey(grid_size)] = start_node

    while (openlist.qsize() > 0):

            # getting the node to expand
        LCNode = openlist.get()         # least cost node
        node2exp = LCNode[1]

        # checking if the node2exp is the goal
        if node2exp.childnum == traj_lim:

            return [node2exp, closelist]

        # expanding the node
        succs = node2exp.getSuccs(r_map, grid_size)

        for item in succs:
            if item.gethashKey(grid_size) in closelist:
                # print 'duplicate ', item.gethashKey(grid_size) , ' is the key'
                continue
            if item.gethashKey(grid_size) in openlist_f:
                # print 'duplicate in open list'
                continue
            # printNode(item)
            openlist.put((item.gcost, item))
            openlist_f[item.gethashKey(grid_size)] = item

        # moving the expanded node to close list, and removing from open list
        # dict
        closelist[node2exp.gethashKey(grid_size)] = node2exp
        # del openlist_f[node2exp.gethashKey(grid_size)]

    return 0


def printNode(node):

    print node.x, node.y
    # print Node.gethashKey(grid_size)

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
    out = astar([startx, starty, startTheta], [goalx, goaly, goalTheta], w)
    if out == 0:
        print 'failure'
    else:
        print 'success'
