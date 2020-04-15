""" File containing the cell object. """


class Cell:
	""" Make a cell.

	Methods
	-------
	__init__

	Attributes
	----------
	content: str
	position: tuple of int or None
	"""
	def __init__(self, content='empty', position=None):
		""" Initalize a cell.

        If not specified the cell is empty and the position is None.
        """
		self.content = content
		self.position = position