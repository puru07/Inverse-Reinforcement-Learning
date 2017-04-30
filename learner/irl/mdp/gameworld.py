"""
Implements the Gameworld MDP.

Puru Rastogi, 2017
pururastogi@gmail.com

Derived from the works of
Matthew Alger, 2015
matthew.alger@anu.edu.au
"""

import numpy as np
import numpy.random as rn
from irl.mdp.gamestate import gamestate as gstate
from irl.mdp.gamestate import arenastate as astate
import commons.parser as parser
from itertools import product


class Gameworld(object):
    """
    Game world MDP.
    """

    def __init__(self, grid_size, arena_st, discount=0.1):
        """
        grid_size: Grid size. int.
        wind: Chance of moving randomly. float.
        ->discrete : discretization of disttance of elements
        discount: MDP discount. float.

        -> Gridworld
        """

        self.actions = ((1, 0), (0, 1), (-1, 0), (0, -1), (0, 0))
        self.n_actions = len(self.actions)
        self.n_states = grid_size**2
        self.grid_size = grid_size
        self.wind = 0.1
        self.discount = discount
        self.arena = arena_st
        self.point = arena_st.point

        # Preconstruct the transition probability array.
        self.transition_probability = np.array([[[self._transition_probability(i, j, k)
            for k in range(self.n_states)]
            for j in range(self.n_actions)]
            for i in range(self.n_states)])

    def __str__(self):
        return "Gameworld({}, {}, {})".format(self.grid_size, self.wind, self.discount)
    
    def getVelFeatures(self,state):
        sameV = 0
        diffV = 0
        staticV = 0
        if (state.Vel == 4 or state.preVel == 4):
            return (0,0,1)
        elif (state.Vel != state.preVel) :
            return (0,1,0)
        else:
            return (1,0,0)

    def dlessFeature(self,state,arena,mode="noghost"):
        '''
        Finding the dimensionless features
        Feature Vector: 
        (all distances are manhattan and normaliszed by gridsize)
        -> distance from the nearest point
        -> summation of distance from all the points
        -> distance from the nearest obstacle
        -> summation of distance from all the obstacles
        -> distance from the nearest ghost
        -> summation of distance from all the ghosts

        => velocity features
        -> same velocity
        -> different velocity
        -> stationary either previously or currently
        '''

        player = state.player
        nghost = len(state.ghost)
        nobs = len(arena.obs)
        npoint = len(state.point)

        dpoint = []                    # distance from each point
        for (x,y) in state.point:
            if (x>=0 and  y >=0):
                dpoint.append([abs(int(x)- player[0]), abs(int(y)- player[1])])
            else:
                dpoint.append([0,0])

        dobs = []                      # distance from each obstacle
        for (x,y) in  arena.obs:
            dobs.append([abs(x- player[0]), abs(y- player[1])])

        dghost = []                     # distance from each ghost
        if mode == "withghost" :
            for (x,y) in state.ghost:
                dghost.append([abs(int(x)- player[0]), abs(int(y)- player[1])])
            f = np.zeros(6)
            f[0] = min(x+y for x,y in dpoint)/(self.grid_size*2.0)
            f[1] = sum(x+y for x,y in dpoint)/(npoint*self.grid_size*2.0)
            f[2] = min(x+y for x,y in dobs)/(self.grid_size*2.0)
            f[3] = sum(x+y for x,y in dobs)/(nobs*self.grid_size*2.0)
            f[4] = min(x+y for x,y in dghost)/(self.grid_size*2.0)
            f[5] = sum(x+y for x,y in dghost)/(nghost*self.grid_size*2.0)
        elif mode == "noghost":
            f = np.zeros(4)
            f[0] = min(x+y for x,y in dpoint)/(self.grid_size*2.0)
            f[1] = sum(x+y for x,y in dpoint)/(npoint*self.grid_size*2.0)
            f[2] = (min(x+y for x,y in dobs))/(self.grid_size*2.0)
            f[3] = sum(x+y for x,y in dobs)/(nobs*self.grid_size*2.0)
        elif mode == "velnoghost":
            f = np.zeros(7)
            f[0] = min(x+y for x,y in dpoint)/(self.grid_size*2.0)
            f[1] = sum(x+y for x,y in dpoint)/(npoint*self.grid_size*2.0)
            f[2] = (min(x + y for x , y in dobs) + 1) / (self.grid_size * 2.0)
            f[3] = sum(x + y for x , y in dobs) / (nobs * self.grid_size * 2.0)
            f[4], f[5], f[6] = self.getVelFeatures(state)

        return f

    def feature_vector(self, i, feature_map,state,arena,mode = "noghost"):
        """
        Get the feature vector associated with a state integer.

        i: State int.
        feature_map: Which feature map to use (default ident). String in {ident,
            coord, proxi}.
        -> Feature vector.
        """
        if feature_map == "dless":
            f = self.dlessFeature(state,arena,mode)
            return f

        if feature_map == "coord":
            f = np.zeros(self.grid_size)
            x, y = i % self.grid_size, i // self.grid_size
            f[x] += 1
            f[y] += 1
            return f
        if feature_map == "proxi":
            f = np.zeros(self.n_states)
            x, y = i % self.grid_size, i // self.grid_size
            for b in range(self.grid_size):
                for a in range(self.grid_size):
                    dist = abs(x - a) + abs(y - b)
                    f[self.point_to_int((a, b))] = dist
            return f
        # Assume identity map.
        f = np.zeros(self.n_states)
        f[i] = 1
        return f

    def feature_matrix(self, arena,feature_map="ident",mode="noghost"):
        """
        Get the feature matrix for this gridworld.

        feature_map: Which feature map to use (default ident). String in {ident,
            coord, proxi}.
        -> NumPy array with shape (n_states, d_states).
        """

        features = []
        if mode == "velnoghost" :
            for n in range (self.n_states):
                for i , j in product(range(5),range(5)):
                    x,y = parser.abs2xy(n,self.grid_size)
                    state = gstate((x,y),(),self.arena.point,i,j)
                    f = self.feature_vector(n, feature_map, state,arena,mode)
                    features.append(f)
        else:
            for n in range(self.n_states):
                x,y = parser.abs2xy(n,self.grid_size)
                state = gstate((x,y),(),self.arena.point)
                f = self.feature_vector(n, feature_map, state,arena,mode)
                features.append(f)
        
        return np.array(features)

    def int_to_point(self, i):
        """
        Convert a state int into the corresponding coordinate.

        i: State int.
        -> (x, y) int tuple.
        """   

        return (i % self.grid_size, i // self.grid_size)

    def point_to_int(self, p):
        """
        Convert a coordinate into the corresponding state int.

        p: (x, y) tuple.
        -> State int.
        """

        return p[0] + p[1]*self.grid_size

    def neighbouring(self, i, k):
        """
        Get whether two points neighbour each other. Also returns true if they
        are the same point.

        i: (x, y) int tuple.
        k: (x, y) int tuple.
        -> bool.
        """

        return abs(i[0] - k[0]) + abs(i[1] - k[1]) <= 1

    def _transition_probability(self, i, j, k):
        """
        Get the probability of transitioning from state i to state k given
        action j.

        i: State int.
        j: Action int.
        k: State int.
        -> p(s_k | s_i, a_j)
        """

        xi, yi = self.int_to_point(i)
        xj, yj = self.actions[j]
        xk, yk = self.int_to_point(k)

        if not self.neighbouring((xi, yi), (xk, yk)):
            return 0.0

        # Is k the intended state to move to?
        if (xi + xj, yi + yj) == (xk, yk):
            return 1 - self.wind + self.wind/self.n_actions

        # If these are not the same point, then we can move there by wind.
        if (xi, yi) != (xk, yk):
            return self.wind/self.n_actions

        # If these are the same point, we can only move here by either moving
        # off the grid or being blown off the grid. Are we on a corner or not?
        if (xi, yi) in {(0, 0), (self.grid_size-1, self.grid_size-1),
                        (0, self.grid_size-1), (self.grid_size-1, 0)}:
            # Corner.
            # Can move off the edge in two directions.
            # Did we intend to move off the grid?
            if not (0 <= xi + xj < self.grid_size and
                    0 <= yi + yj < self.grid_size):
                # We intended to move off the grid, so we have the regular
                # success chance of staying here plus an extra chance of blowing
                # onto the *other* off-grid square.
                return 1 - self.wind + 2*self.wind/self.n_actions
            else:
                # We can blow off the grid in either direction only by wind.
                return 2*self.wind/self.n_actions
        else:
            # Not a corner. Is it an edge?
            if (xi not in {0, self.grid_size-1} and
                yi not in {0, self.grid_size-1}):
                # Not an edge.
                return 0.0

            # Edge.
            # Can only move off the edge in one direction.
            # Did we intend to move off the grid?
            if not (0 <= xi + xj < self.grid_size and
                    0 <= yi + yj < self.grid_size):
                # We intended to move off the grid, so we have the regular
                # success chance of staying here.
                return 1 - self.wind + self.wind/self.n_actions
            else:
                # We can blow off the grid only by wind.
                return self.wind/self.n_actions

    def reward(self, state_int):
        """
        Reward for being in state state_int.

        state_int: State integer. int.
        -> Reward.
        """

        if state_int == self.n_states - 1:
            return 1
        return 0

    def average_reward(self, n_trajectories, trajectory_length, policy):
        """
        Calculate the average total reward obtained by following a given policy
        over n_paths paths.

        policy: Map from state integers to action integers.
        n_trajectories: Number of trajectories. int.
        trajectory_length: Length of an episode. int.
        -> Average reward, standard deviation.
        """

        trajectories = self.generate_trajectories(n_trajectories,
                                             trajectory_length, policy)
        rewards = [[r for _, _, r in trajectory] for trajectory in trajectories]
        rewards = np.array(rewards)

        # Add up all the rewards to find the total reward.
        total_reward = rewards.sum(axis=1)

        # Return the average reward and standard deviation.
        return total_reward.mean(), total_reward.std()

    def optimal_policy(self, state_int):
        """
        The optimal policy for this gridworld.

        state_int: What state we are in. int.
        -> Action int.
        """

        sx, sy = self.int_to_point(state_int)

        if sx < self.grid_size and sy < self.grid_size:
            return rn.randint(0, 2)
        if sx < self.grid_size-1:
            return 0
        if sy < self.grid_size-1:
            return 1
        raise ValueError("Unexpected state.")

    def optimal_policy_deterministic(self, state_int):
        """
        Deterministic version of the optimal policy for this gridworld.

        state_int: What state we are in. int.
        -> Action int.
        """

        sx, sy = self.int_to_point(state_int)
        if sx < sy:
            return 0
        return 1

    def generate_trajectories(self, n_trajectories, trajectory_length, policy,
                                    random_start=False):
        """
        Generate n_trajectories trajectories with length trajectory_length,
        following the given policy.

        n_trajectories: Number of trajectories. int.
        trajectory_length: Length of an episode. int.
        policy: Map from state integers to action integers.
        random_start: Whether to start randomly (default False). bool.
        -> [[(state int, action int, reward float)]]
        """

        trajectories = []
        for _ in range(n_trajectories):
            if random_start:
                sx, sy = rn.randint(self.grid_size), rn.randint(self.grid_size)
            else:
                sx, sy = 0, 0

            trajectory = []
            for _ in range(trajectory_length):
                if rn.random() < self.wind:
                    action = self.actions[rn.randint(0, 4)]
                else:
                    # Follow the given policy.
                    action = self.actions[policy(self.point_to_int((sx, sy)))]

                if (0 <= sx + action[0] < self.grid_size and
                        0 <= sy + action[1] < self.grid_size):
                    next_sx = sx + action[0]
                    next_sy = sy + action[1]
                else:
                    next_sx = sx
                    next_sy = sy

                state_int = self.point_to_int((sx, sy))
                action_int = self.actions.index(action)
                next_state_int = self.point_to_int((next_sx, next_sy))
                reward = self.reward(next_state_int)
                trajectory.append((state_int, action_int, reward))

                sx = next_sx
                sy = next_sy

            trajectories.append(trajectory)

        return np.array(trajectories)
