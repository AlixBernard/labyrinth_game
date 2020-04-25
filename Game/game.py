""" File containing the game object. """


from random import random, choice, sample

from labyrinth import Labyrinth
from player import Player
from weapon import Weapon


class Game:
    """ Class of a game of "The Labyrinth".

    Attributes
    ----------
    game_over: bool
    labyrinth: labyrinth
    turn: int
    players: dict
    options: list of bool
    weapons: dict

    Methods
    -------
    __init__
    set_weapons
    randomly_place_players
    is_move_possible
    move_player
    shoot
    player_hit
    activate_cell
    is_game_over
    """
    def __init__(self, labyrinth: Labyrinth, players: list, options=None):
        """ Initialize a game according to the parameters entered. """
        self.game_over = False
        self.labyrinth = labyrinth
        self.turn = 0
        self.players = players
        self.weapons = {'pistol': Weapon('pistol', 2, 5), 'shotgun': Weapon('shotgun', 3, 2)}


    def display_rules(self):
        """ Display the labyrinth game's rules. """
        print()
        print("***************************************")
        print("********* THE LABYRINTH GAME **********")
        print("***************************************")
        print("\nRules:")
        print("- Be 1 to 4 players.")
        print("- Find your way around a labyrinth to find the treasure and exit with it to win.")
        print("- Alternatively find a weapon and kill all other players to win.")
        print("\nCommands:")
        print("- move <direction>")
        print("shortcuts: w, s, a, d")
        print("- shoot <direction>")
        print("- activate cell")
        print("shortcut: e")
        print("- exit")
        print("\nDirections: up, down, left, right\n")
        print("That is all you need to know!")
        print("Good luck to escape, you will need it...\n")


    def set_weapons(self):
        """ Set weapons accroding to the user. """
        weapons = {}

        more_weapons = True
        while more_weapons:
            name = input('Enter the weapon name: ')
            damage = int(input('Enter the weapon damage: '))
            weapons[name] = damage

            if input('Add another weapon? (y/n)\t\t').lower() in ['n', 'no']: more_weapons = False

        self.weapons = weapons
    

    def randomly_place_players(self):
        """ Attribute random position to the players.

        Players are not placed on cells with special content.
        """
        spec_contents = ['river', 'exit', 'treasure', 'map', 'arsenal', 'wormhole', 'hospital']
        possible_positions = [pos for pos, cell in self.labyrinth.cells.items()
                                  if cell.content not in spec_contents]

        positions = sample(possible_positions, k=len(self.players))
        for player, pos in zip(self.players, positions): self.players[player].position = pos
    

    def is_move_possible(self, player: Player, move: str):
        """ Return if the move is possible and the reason why.

        If the players asked to exit the game it is executed here as well.
        """
        if move == 'skip': return True, 'Just chill out man'

        if move[:4] == 'move' or move in ['w', 's', 'a', 'd']:
            direction = move[5:]
            if move == 'w' or direction == 'up': x_move, y_move = 0, 1
            if move == 's' or direction == 'down': x_move, y_move = 0, -1
            if move == 'a' or direction == 'left': x_move, y_move = -1, 0
            if move == 'd' or direction == 'right': x_move, y_move = 1, 0
            x, y = self.players[player].position
            if (x + x_move, y + y_move) in self.labyrinth.cells.keys():
                if self.labyrinth.junctions[(self.labyrinth.cells[x, y],
                                             self.labyrinth.cells[x + x_move, y + y_move])] != 'wall':
                    return True, 'Because I say so'
                return False, 'A wall prevents you to move in that direction'
            return False, 'The monolith prevents you to move in that direction'

        if move[:5] == 'shoot':
            weapon = self.players[player].weapon 
            if weapon != None and weapon.name in ['pistol', 'shotgun']:
            	return True, 'Because you are armed to the teeth!'
            return False, 'You do not have anything to shoot, go home..!'

        if move == 'activate cell' or move == 'e':
            if self.labyrinth.cells[self.players[player].position] != 'empty':
                return True, 'This cell is not empty.'
            return False, 'There is nothing in this room, try again.'

        return False, 'Move not recognized'
    

    def move_player(self, player: Player, direction: str):
        """ Modify a player's position and describe the room. """
        if direction == 'w' or direction == 'up': x_move, y_move = 0, 1
        if direction == 's' or direction == 'down': x_move, y_move = 0, -1
        if direction == 'a' or direction == 'left': x_move, y_move = -1, 0
        if direction == 'd' or direction == 'right': x_move, y_move = 1, 0

        x, y = self.players[player].position
        self.players[player].position = (x + x_move, y + y_move)
        content = self.labyrinth.cells[self.players[player].position].content

        if content == 'empty': print(player + ' is now in an empty room.')
        if content == 'arsenal': print(player + ' is now now in an arsenal.')
        if content == 'wormhole': print(player + ' is now in a room containing a wormhole.')
        if content == 'treasure': print(player + ' is now in the treasure room.')
        if content == 'map': print(player + ' is now in the map room.')
        if content == 'exit':
            if self.players[player].carry:
                print(player + ' is now in the exit room and can leave.')
            else: print(player + ' is now in the exit room but you need the treasure to leave.')
        for p in self.players:
            if p != player and self.players[p].position == self.players[player].position:
                print(player + ' finds itself in the same room as ' + p)
    

    def shoot(self, player: Player, direction: str):
        """ Check if another player is hit by player and describe what happens. """
        if direction == 'up': x_move, y_move = 0, 1
        if direction == 'down': x_move, y_move = 0, -1
        if direction == 'left': x_move, y_move = -1, 0
        if direction == 'right': x_move, y_move = 1, 0

        # If another player is present in the same cell, hit it and quit method.
        x1, y1 = self.players[player].position
        for p in self.players:
            if p != player and self.players[p].position == (x1, y1):
                self.player_hit(p, self.players[player].weapon)
                return 0

        # If the direction shooting at is directly a monolith then describe what happens.
        x2, y2 = x1 + x_move, y1 + y_move
        if (x2, y2) not in self.labyrinth.cells.keys():
            print('The bullet hit a wall')
            return 0

        # Check cells one by one in the direction to see if a player is there and hit it if so.
        # Stops if the cell is to far for the weapon's distance and describe what happens.
        c1, c2 = self.labyrinth.cells[x1, y1], self.labyrinth.cells[x2, y2]
        distance = 0
        while (x2, y2) in self.labyrinth.cells.keys() and self.labyrinth.junctions[c1, c2] != 'wall':
            
            distance += 1
            if distance > self.players[player].weapon.distance:
                print('Nothing happens')
                return 0
            
            for p in self.players:
                if self.players[p].status == 'dead': continue
                if self.players[p].position == (x2, y2):
                    self.player_hit(p, self.players[player].weapon)
                    return 0
            
            x1, y1 = x2, y2
            x2, y2 = x1 + x_move, y1 + y_move
            if (x2, y2) not in self.labyrinth.cells.keys():
                print('The bullet hit a wall')
                return 0
            c1, c2 = self.labyrinth.cells[x1, y1], self.labyrinth.cells[x2, y2]
        print('The bullet hit a wall')
    

    def player_hit(self, player: Player, weapon: Weapon):
        """ Change player's status according to the weapon damage, describes what happened. """
        status = self.players[player].status
        if weapon.damage == 3: self.players[player].status = 'dead'

        if weapon.damage == 2:
            if status != 'healthy': self.players[player].status = 'dead'
            else: self.players[player].status = 'wounded'

        if not self.players[player].carry:
            print(player + ' got hit, and is now ' + self.players[player].status)
        else:
            self.labyrinth.cells[self.players[player].position].content = 'treasure'
            print(player + ' got hit, dropped the treasure, and is now ' + self.players[player].status)

    
    def activate_cell(self, player: Player):
        """ Execute the cell action.

        If the cell contains an arsenal then the player pick up a random weapon.
        If the cell contains the treasure then the player pick it up.
        Describe what happens.
        """
        content = self.labyrinth.cells[self.players[player].position].content
        pos = self.labyrinth.cells[self.players[player].position].position

        if content == 'map':
            print('You approach some strange writing on a rock and understand it is a map.')
            self.labyrinth.display_labyrinth()

        if content == 'arsenal':
            if random() < .5: weapon = 'pistol'
            else: weapon = 'shotgun'
            self.players[player].weapon = self.weapons[weapon]
            print('You picked up a ' + weapon)

        if content == 'wormhole':
            for i in range(len(self.labyrinth.wormholes)):
                if self.labyrinth.wormholes[i] == self.labyrinth.cells[pos]:
                    new_pos = self.labyrinth.wormholes[(i + 1) % len(self.labyrinth.wormholes)].position
                    self.players[player].position = new_pos
                    print('As you approach the wormhole you fear the unknown '
                           + 'but due to your lack of common sense you still get in '
                           + 'and after what seems to be an eternity you finally exit from another wormhole.')
            
            for p in self.players:
                if p != player and self.players[p].position == self.players[player].position:
                    print('You find yourself in the same room as ' + p)


        if content == 'treasure':
            self.players[player].carry = True
            self.labyrinth.cells[self.players[player].position].content = 'empty'
            print('You now carry the treasure')

        if content == 'empty': print('Nothing happens')


    def move_bear_npc(self):
        """ Move randomly the bear npc player and hurt/move other players if on same case. """
        while True:
            direction = choice(['up', 'down', 'left', 'right'])

            if direction == 'up': x_move, y_move = 0, 1
            if direction == 'down': x_move, y_move = 0, -1
            if direction == 'left': x_move, y_move = -1, 0
            if direction == 'right': x_move, y_move = 1, 0

            x, y = self.players['Bear NPC'].position
            if (x + x_move, y + y_move) in self.labyrinth.cells.keys():
                if self.labyrinth.junctions[(self.labyrinth.cells[x, y],
                                             self.labyrinth.cells[x + x_move, y + y_move])] != 'wall':
                    self.players['Bear NPC'].position = x + x_move, y + y_move
                    break

            for player in self.players:
                if player == 'Bear NPC': continue
                if self.players[player].position == self.players['Bear NPC'].position:
                    self.player_hit(player, Weapon('Bear paw', 2, 0))
                    while True:
                        direction = choice(['up', 'down', 'left', 'right'])
                        if self.is_move_possible(player, 'move ' + direction): break
                    self.move_player(player, direction)



    def river_move_player(self, player: Player):
        """ Move a player two cells down the river flow unless if at the end. """
        idx = 0
        for cell in self.labyrinth.river:
            if cell == self.labyrinth.cells[self.players[player].position]: break
            idx += 1

        if idx == len(self.labyrinth.river) - 1:
            if player == 'Bear NPC': return 0
            print('The strong current shakes you but you stay in place.')
            return 0

        for i in range(2):
            if idx < len(self.labyrinth.river) - 1:
                self.players[player].position = self.labyrinth.river[(idx + 1)].position
                idx += 1
        if player == 'Bear NPC': return 0
        print('The strong current of the river moves you down stream.')
    

    def is_game_over(self):
        """ Return True if a player has won the game and describe it. """
        dead_count = 0
        players_alive = []

        # Check if a player has escaped with the treasure and describes it if so.
        # Also count dead players.
        for player in self.players:
            if self.players[player].position == self.labyrinth.exit_cell.position and self.players[player].carry:
                reason = player + ' escapes with the treasure and wins!'
                return True, reason
            if self.players[player].status == 'dead':
                dead_count += 1
            else: players_alive.append(player)

        # If only one player is playing then do not consider being the only one left alive as a win
        if len(self.players) == 1 or (len(self.players) == 2 and 'Bear NPC' in self.players):
            reason = 'You have to find the treasure and exit!'
            return False, reason

        # Check if all players but one are dead and describes it if so.
        if dead_count == len(self.players) - 1:
            reason = players_alive[0] + ' is the only player alive and wins, congrats you murderer!'
            return True, reason

        # Describe why the game is not over.
        reason = ''
        for i in [len(players_alive) - j for j in range(1, len(players_alive) + 1)]:
            if i == 1: reason += player + ', and '
            elif i == 0: reason += player + ' are still alive and no one left the labyrinth with the treasure'
            else: reason += player + ', '
        return False, reason