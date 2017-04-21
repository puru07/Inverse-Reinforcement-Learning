class gamestate():
    """
    State of the game at each point
    """
    state.ghost = (())
    state.point = (())
    state.player = ()
    state.obs = (())

    def __init__(self, player,ghost_tup, obs_tup,points_tup):
    	self.player = player
    	self.points = points_tup
    	self.obs = obs_tup
    	self.ghost = ghost_tup
