""" File containing the player object. """


from weapon import Weapon


class Player:
	""" Player object. 

	Attributes
	----------
	status: str
	position: tuple of int
	carry: bool
	weapon: weapon
	
	Methods
	-------
	__init__
	"""
	def __init__(self, position=None, status='healthy', weapon=None, carry=False):
		""" Initialize a player. """
		self.status = status
		self.weapon = weapon
		self.carry = carry
		self.position = position