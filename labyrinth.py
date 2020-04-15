""" File containing the labyrinth object. """


import random as rand

from cell import Cell


class Labyrinth:
    """ Make a labyrinth.

    Methods
    -------
    __init__

    Attributes
    ----------
    size: int
    cells: dict
    treasure_cell: cell
    ext_cell: cell
    junctions: dict
    """


    def __init__(self, size: int):
        """ Initialize a labyrinth.
        
        Make a square labyrinth of the specified size containing one treasure and one exit.
        Each other cell has a probability of being: empty with 80%, an arsenal of 20%.
        """
        self.size = size
        self.cells = self._init_cells(.15)
        self.treasure_cell = self._get_treasure_cell()
        self.exit_cell = self._get_exit_cell()
        self.junctions = self._init_junctions(.4)
        self._find_or_open_new_cell_until_all_accessible({self.exit_cell.position: self.exit_cell})

    
    def _init_cells(self, arsenal_p: float, wormhole_p=0, river_p=0, hospital_p=0):

        cells = {(x, y): Cell(position=(x, y)) for x in range(self.size) for y in range(self.size)}
        for cell in cells.values():
            if rand.random() < arsenal_p: cell.content = 'arsenal'

        treasure_pos = rand.choice(list(cells.keys()))
        cells[treasure_pos].content = 'treasure'

        possible_exits = [cells[x, y] for x in range(self.size) for y in range(self.size)
                                      if x in [0, self.size - 1] or y in [0, self.size - 1]]
        exit_pos = treasure_pos
        while exit_pos == treasure_pos: exit_pos = rand.choice(possible_exits).position
        cells[exit_pos].content = 'exit'

        return cells


    def _get_exit_cell(self):

        for cell in self.cells.values():
            if cell.content == 'exit': return cell
        raise valueError('There are no exit present in the labyinth')


    def _get_treasure_cell(self):

        for cell in self.cells.values():
            if cell.content == 'treasure': return cell
        raise valueError('There are no exit present in the labyinth')


    def _init_junctions(self, wall_p: float):
        junctions = {(c1, c2): 'nothing' for c1 in self.cells.values()
                                                           for c2 in self.cells.values()
                                                           if c1 != c2}
        junctions_to_del = []
        for c1, c2 in junctions.keys():
            x1, y1 = c1.position
            x2, y2 = c2.position

            if abs(x2 - x1) + abs(y2 - y1) == 1:
                if rand.random() < wall_p:
                    junctions[c1, c2] = 'wall'
                    junctions[c2, c1] = junctions[c1, c2]
            else: junctions_to_del.append((c1, c2))

        for c1, c2 in junctions_to_del: del junctions[c1, c2]

        return junctions


    def _are_neighbouring_cells(self, c1, c2):
        """ Return True if c2 is above, under, left, or right of c1, False otherwise. """
        x1, y1 = c1.position
        x2, y2 = c2.position

        if abs(x2 - x1) + abs(y2 - y1) == 1: return True
        else: return False


    def _find_or_open_new_cell_until_all_accessible(self, accessible_cells: dict):
        """ Find a new accessible cell or open a wall to do so until all cells are accessibles.  """
        # First we try to find a new 'natural' acessible cell.
        new_accessible_cell_found = False
        for c1 in accessible_cells.values():
            x1, y1 = c1.position

            for c2 in self.cells.values():
                x2, y2 = c2.position

                if c2 in accessible_cells.values(): continue

                if self._are_neighbouring_cells(c1, c2):
                    if self.junctions[c1, c2] == 'nothing':
                        accessible_cells[c2.position] = c2
                        new_accessible_cell_found = True
                        break
                    possible_new_cell_junction = c1, c2

            if new_accessible_cell_found: break

        # If we haven't found a new 'natural' accessible cell
        # then a wall next to an accessible cell is opened.
        if not new_accessible_cell_found:
            c1, c2 = possible_new_cell_junction
            self.junctions[c1, c2] = 'nothing'
            self.junctions[c2, c1] = 'nothing'
            accessible_cells[c2.position] = c2

        if accessible_cells != self.cells:
            accessible_cells = self._find_or_open_new_cell_until_all_accessible(accessible_cells)

        return accessible_cells