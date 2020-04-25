""" File containing the labyrinth object. """


from random import random, choice, sample

from cell import Cell


class Labyrinth:
    """ Make a labyrinth.

    Attributes
    ----------
    size: int
    nb_player_starters: int
    cells: dict
    treasure_cell: cell
    ext_cell: cell
    junctions: dict

    Methods
    -------
    __init__
    display_labyrinth
    """


    def __init__(self, size: int, nb_player_starters: int, options=None):
        """ Initialize a labyrinth.
        
        Make a square labyrinth of the specified size containing one treasure and one exit.
        The parameter options must be a dictionary if specified.
        """
        self.size = size
        self.nb_player_starters = nb_player_starters

        self.options = {'wormhole': False, 'river': False, 'bear': False, 'hospital': False}
        if options != None:
            for opt, val in options.items():
                if opt in self.options.keys():
                    self.options[opt] = val

        self.wormholes = []
        self.river = []
        self._init_cells(.05)
        self.treasure_cell = self._get_treasure_cell()
        self.exit_cell = self._get_exit_cell()
        self.junctions = self._init_junctions(.4)
        self._open_labyrinth({self.exit_cell.position: self.exit_cell})
        print(50 * ' ')


    def _init_cells(self, arsenal_p: float):

        # Create all cells as empty.
        print('Creating empty labyrinth...', end='\r')
        self.cells = {(x, y): Cell(position=(x, y)) for x in range(self.size)
                                                    for y in range(self.size)}

        spec_contents = ['river', 'exit', 'treasure', 'map', 'arsenal', 'wormhole', 'hospital']

        # Make river if option is on.
        if self.options['river']:
            print('Filling up the river...' + 30 * ' ', end='\r')
            river_size_min = ((self.size - 1)**2 // 4) + 1 
            river_size_max = self.size**2 // 4
            river_sizes = list(range(river_size_min - 1, river_size_max + 1))
            possible_source_cells = [cell for cell in self.cells.values()
                                          if self._is_edge_cell(cell)
                                             and not self._is_corner_cell(cell)]
            river = [choice(possible_source_cells)]
            while True:

                if len(river) in river_sizes: cell_can_be_edge = True
                else: cell_can_be_edge = False

                cell = self._choose_next_river_cell(river, cell_can_be_edge=cell_can_be_edge)

                if cell == None or len(river) > river_size_max:
                    river = [river[0]]
                    continue

                river.append(cell)

                if cell_can_be_edge and self._is_edge_cell(cell): break

            for c in river: self.cells[c.position].content = 'river'
            self.river = river

        # Let the user know what is happening.
        print('Set up specific cells...' + 30 * ' ', end='\r')

        # Set the exit cell..
        exit_pos = choice([pos for pos, cell in self.cells.items()
                               if self._is_edge_cell(cell) and
                                  cell.content not in spec_contents])
        self.cells[exit_pos].content = 'exit'

        # Set the treasure in a cell.
        treasure_pos = choice([pos for pos, cell in self.cells.items()
                                   if cell.content not in spec_contents])
        self.cells[treasure_pos].content = 'treasure'

        # Set the map cell.
        map_pos = choice([pos for pos, cell in self.cells.items()
                              if cell.content not in spec_contents])
        self.cells[map_pos].content = 'map'

        # Set arsenal cells.
        arsenals_nb_min = (self.size - 1)**2 // 4
        arsenals_nb_max = self.size**2 // 4
        arsenal_nb = choice(list(range(arsenals_nb_min, arsenals_nb_max + 1)))
        for i in range(arsenal_nb):
            arsenal_pos = choice([pos for pos, cell in self.cells.items()
                                      if cell.content not in spec_contents])
            self.cells[arsenal_pos].content = 'arsenal'

        # Set wormholes if option is on.
        if self.options['wormhole']:
            print('Ripping space time appart in some locations...' + 30 * ' ', end = '\r')
            nb_wormholes = self.size // 2
            for i in range(nb_wormholes):
                content = 'exit'
                while content in spec_contents:
                    pos = choice(list(self.cells.keys()))
                    content = self.cells[pos].content
                self.cells[pos].content = 'wormhole'
                self.wormholes.append(self.cells[pos])


    def _choose_next_river_cell(self, river: list, cell_can_be_edge=True):

        c0 = river[-1]
        adjacent_c0 = []

        # Get a list of adjacent cells (with or without edge cells).
        if cell_can_be_edge:
            for cell in self.cells.values():
                if self._are_adjacent_cells(cell, c0): adjacent_c0.append(cell)
        else:
            for cell in self.cells.values():
                if self._are_adjacent_cells(cell, c0) and not self._is_edge_cell(cell):
                    adjacent_c0.append(cell)

        # Randomize the order of the list.
        adjacent_c0 = sample(adjacent_c0, k=len(adjacent_c0))

        # Ensure that the adjacent cells are not part of the river.
        for c1 in adjacent_c0:

            adjacent_c1 = []
            for cell in self.cells.values():
                if self._are_adjacent_cells(cell, c1): adjacent_c1.append(cell)

            are_river = [cell in river for cell in adjacent_c1
                                       if cell != c0]
            if True in are_river: continue

            return c1

        return None


    def _get_exit_cell(self):

        for cell in self.cells.values():
            if cell.content == 'exit': return cell


    def _get_treasure_cell(self):

        for cell in self.cells.values():
            if cell.content == 'treasure': return cell


    def _init_junctions(self, wall_p: float):

        junctions = {(c1, c2): 'nothing' for c1 in self.cells.values()
                                         for c2 in self.cells.values()
                                         if c1 != c2}
        junctions_to_del = []
        for c1, c2 in junctions.keys():
            x1, y1 = c1.position
            x2, y2 = c2.position

            if abs(x2 - x1) + abs(y2 - y1) == 1:
                if random() < wall_p and c1 not in self.river and c2 not in self.river:
                    junctions[c1, c2] = 'wall'
                    junctions[c2, c1] = junctions[c1, c2]
            else: junctions_to_del.append((c1, c2))

        for c1, c2 in junctions_to_del: del junctions[c1, c2]

        return junctions


    def _is_edge_cell(self, cell: Cell):
        """ Return True if the cell is on the edge of the labyrinth, False otherwise. """
        x, y = cell.position
        if x in [0, self.size - 1] or y in [0, self.size - 1]: return True
        return False


    def _is_corner_cell(self, cell: Cell):
        """ Return True if the cell is is a corner of the labyrinth, False otherwise. """
        x, y = cell.position
        if x in [0, self.size - 1] and y in [0, self.size - 1]: return True
        return False


    def _are_adjacent_cells(self, c1: Cell, c2: Cell):
        """ Return True if c2 is above, under, left, or right of c1, False otherwise. """
        x1, y1 = c1.position
        x2, y2 = c2.position

        if abs(x2 - x1) + abs(y2 - y1) == 1: return True
        return False


    def _open_labyrinth(self, accessible_cells: dict):
        """ Find a new accessible cell or open a wall to do so until all cells are accessibles.  """
        # First we try to find a new 'natural' acessible cell.
        print('Opening the world...' + 30 * ' ', end='\r')

        cells_to_link = {c.position: c for c in self.cells.values()
                                       if c.content != 'river' or c == self.river[-1]}
        new_accessible_cell_found = False
        for c1 in accessible_cells.values():
            x1, y1 = c1.position

            for c2 in cells_to_link.values():
                x2, y2 = c2.position

                if c2 in accessible_cells.values(): continue

                if self._are_adjacent_cells(c1, c2):
                    if self.junctions[c1, c2] == 'nothing':
                        accessible_cells[c2.position] = c2
                        new_accessible_cell_found = True
                        break
                    possible_new_cell_junction = c1, c2

            if new_accessible_cell_found: break

        # If we haven't found a new 'natural' accessible cell
        # then a wall next to an accessible cell is opened.
        try:
            if not new_accessible_cell_found:
                c1, c2 = possible_new_cell_junction
                self.junctions[c1, c2] = 'nothing'
                self.junctions[c2, c1] = 'nothing'
                accessible_cells[c2.position] = c2
        except:
            if not new_accessible_cell_found:
                if self.river[0] in accessible_cells:
                    for cell in self.river:
                        accessible_cells[cell.position] = cell
                else:
                    # An unlikely event occur that might make the labyrinth unsolvable
                    # however the probability of it being unsolvable despite the event
                    # is low enough to be ignored.
                    return accessible_cells

        if len(accessible_cells) != len(list(cells_to_link.keys())):
            accessible_cells = self._open_labyrinth(accessible_cells)

        return accessible_cells


    def display_labyrinth(self):
        """ Display the labyrinth in the terminal. """
        line = '+'
        for x in range(self.size): line += '+==='
        line += '++'
        print(line)

        for y in [self.size - (i + 1) for i in range(self.size)]:
            line = '||'

            for x in range(self.size):
                content = self.cells[x, y].content

                if content == 'empty': display_cell = '   '
                if content == 'exit': display_cell = ' E '
                if content == 'treasure': display_cell = ' T '
                if content == 'map': display_cell = ' M '
                if content == 'wormhole': display_cell = ' W '
                if content == 'arsenal': display_cell = ' A '
                if content == 'river':
                    if self.cells[x, y] == self.river[0]: display_cell = ' R '
                    else: display_cell = ' ≈ '

                line += display_cell

                if x < self.size - 1:
                    c1 = self.cells[x, y]
                    c2 = self.cells[x + 1, y]
                    if self.junctions[c1, c2] == 'nothing': display_junction = ' '
                    if self.junctions[c1, c2] == 'wall': display_junction = '|'
                    line += display_junction

                if x == self.size - 1: line += '||'

            print(line)

            if y > 0:
                line = '+'
                for x in range(self.size):
                    c1 = self.cells[x, y]
                    c2 = self.cells[x, y - 1]
                    if self.junctions[c1, c2] == 'nothing': display_junction = '+   '
                    if self.junctions[c1, c2] == 'wall': display_junction = '+---'
                    line += display_junction

                line += '++'
                print(line)

            if y == 0:
                line = '+'
                for x in range(self.size): line += '+==='
                line += '++'
                print(line)


    def display_legend(self):
        print(30 * ' ')
        print('- R is the source of the river.')
        print('- ≈ is a river cell.')
        print('- E is the exit.')
        print('- T is the treasure.')
        print('- A is an arsenal.')
        print('- M is the cell containing the map.')
        print('- W is a wormhole')