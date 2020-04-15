""" File containing the weapon object. """


class Weapon:
	""" Weapon object to be used by a player object. 

	Methods
	-------
	__init__

	Attributes
	----------
	name: str
	damage: int
	distance: int
	"""
	def __init__(self, name: str, damage: int, distance: int):
		""" Initialize weapon's attributes. """
		self.name = name
		self.damage = damage
		self.distance = distance