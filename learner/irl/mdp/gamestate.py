class gamestate(object):
    """
    State of the game at each point
    """
    def __init__(self, player,ghost_tup,points_tup):
    	self.player = player 		# and action
    	
    	self.ghost = ghost_tup
        self.point = points_tup


class arenastate(object):
	"""
	Information about the game arena
	"""
	def __init__(self,nghost,npoint,obs_tup):
		self.nghost = nghost
		self.npoint = npoint
		self.obs = obs_tup
    	