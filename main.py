""" File containing the main function and running the game. """


from labyrinth import Labyrinth
from player import Player
from game import Game


def start_game():
    """ Start a game of the labyrinth. 

    Manage players turn until someone win or asked to exit the game.
    """
    display_rules()
    players = get_players()
    size = get_labyrinth_size()
    game = Game(Labyrinth(size), players)
    game.randomly_place_players()
    display_labyrinth(game.labyrinth)

    while not game.game_over:
        for player in game.players:

            if game.players[player].status == 'dead': continue

            move = get_player_move(player)
            move_possible, reason = game.is_move_possible(player, move)
            while not move_possible:
                print(reason)
                move = get_player_move(player)
                move_possible, reason = game.is_move_possible(player, move)

            if move in ['move up', 'move down', 'move left', 'move right']:
                direction = move[5:]
                game.move_player(player, direction)
            if move in ['shoot up', 'shoot down', 'shoot left', 'shoot right']:
                direction = move[6:]
                game.shoot(player, direction)
            if move == 'activate cell':
                game.activate_cell(player)

            game.game_over, reason = game.is_game_over()
            if game.game_over:
                print(reason)
                break

        if not game.game_over: game.turn += 1

    print("\nLabyrinth: finished in {} turns.".format(game.turn))
    display_labyrinth(game.labyrinth)


def display_rules():
    """ Display the labyrinth game's rules. """
    print("***************************************")
    print("********* THE LABYRINTH GAME **********")
    print("***************************************")
    print("\nRules:")
    print("- Be 2 to 4 players.")
    print("- Find your way around a labyrinth to find the treasure and exit with it to win.")
    print("- Alternatively find a weapon and kill all other players to win.")
    print("\nCommands:")
    print("- move <direction>")
    print("- shoot <direction>")
    print("- activate cell")
    print("- exit")
    print("\nDirections: up, down, left, right\n")
    print("That is all you need to know!")
    print("Good luck to escape, you will need it...\n")


def get_players():
    """ Get player names via the user. """
    players = input('Enter the player names separated by a comma: ')
    players = players.split(',')
    for i in range(len(players)): name = players[i].strip()
    players = {name: Player() for name in players}

    return players


def get_labyrinth_size():
    """ Get the labyrinth size via the user.

    Size must be comprised between 4 and 12 included.
    """
    size = 0
    while size not in [str(i) for i in range(4, 13)]:
        size = input('Enter the desired size of labyrinth (must be comprised between 4 and 12): ')
    
    return int(size)


def get_player_move(player):
    """ Get player move via the user.

    The move must be one of the known moves.
    """
    known_moves = ['move up', 'move down', 'move left', 'move right', 'shoot up', 'shoot down',
                   'shoot left', 'shoot right', 'activate cell', 'exit']
    move = input(player + ': ').lower()
    while move not in known_moves: move = input('Command unkown.   ' + player + ': ')
    
    return move


def display_labyrinth(labyrinth):
    """ Display the labyrinth in the terminal. """
    line = '+'
    for x in range(labyrinth.size): line += '+==='
    line += '++'
    print(line)

    for y in [labyrinth.size - (i + 1) for i in range(labyrinth.size)]:
        line = '||'

        for x in range(labyrinth.size):
            content = labyrinth.cells[x, y].content

            if content == 'empty': display_cell = '   '
            if content == 'arsenal': display_cell = ' A '
            if content == 'treasure': display_cell = ' T '
            if content == 'exit': display_cell = ' E '

            line += display_cell

            if x < labyrinth.size - 1:
                c1 = labyrinth.cells[x, y]
                c2 = labyrinth.cells[x + 1, y]
                if labyrinth.junctions[c1, c2] == 'nothing': display_junction = ' '
                if labyrinth.junctions[c1, c2] == 'wall': display_junction = '|'
                line += display_junction

            if x == labyrinth.size - 1: line += '||'

        print(line)

        if y > 0:
            line = '+'
            for x in range(labyrinth.size):
                c1 = labyrinth.cells[x, y]
                c2 = labyrinth.cells[x, y - 1]
                if labyrinth.junctions[c1, c2] == 'nothing': display_junction = '+   '
                if labyrinth.junctions[c1, c2] == 'wall': display_junction = '+---'
                line += display_junction
            line += '++'
            print(line)

        if y == 0:
            line = '+'
            for x in range(labyrinth.size): line += '+==='
            line += '++'
            print(line)


if __name__ == '__main__': start_game()