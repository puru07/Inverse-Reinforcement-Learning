class gamestate(object):
    """
    State of the game at each point
    """

    def __init__(self, player, ghost_tup, points_tup, vel=4, prevel=4):
        self.player = player        # and action
        self.ghost = ghost_tup
        self.point = points_tup
        self.Vel = vel
        self.preVel = prevel


class arenastate(object):
    """
    Information about the game arena
    """

    def __init__(self, nghost, point_tup, obs_tup):
        self.nghost = nghost
        self.point = point_tup
        self.obs = obs_tup
