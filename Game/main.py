""" File containing the main function and running the game. """


from labyrinth import Labyrinth
from player import Player
from game import Game


def play_game_labyrinth():
    """ Start a game of the labyrinth. 

    Manage players turn until someone win or asked to exit the game.
    """
    players = get_players()
    while True:
        size = get_labyrinth_size()
        if size == 4 and len(players) > 4: print('The labyrinth size is too small for the number of players.')
        else: break
    options = get_options()
    game = Game(Labyrinth(size, len(players), options), players)
    if options['bear']: game.players['Bear NPC'] = Player()
    game.randomly_place_players()
    game.display_rules()
    game.labyrinth.display_labyrinth()

    while not game.game_over:
        for player in game.players:

            if game.players[player].status == 'dead': continue

            if player == 'Bear NPC':
                game.move_bear_npc()
                move = 'skip'
            else: move = get_player_move(player)
            
            move_possible, reason = game.is_move_possible(player, move)
            while not move_possible:
                print(reason)

                if move == 'exit':
                    answer = input('Are you sure you want to quit the game? [y/n] ').lower()
                    if answer in ['y', 'yes']: return 0
                    print('That is right, never give up!')

                move = get_player_move(player)
                move_possible, reason = game.is_move_possible(player, move)

            if move == 'skip': pass

            if move in ['move up', 'move down', 'move left', 'move right']:
                direction = move[5:]
                game.move_player(player, direction)
            if move in ['w', 's', 'a', 'd']:
                direction = move
                game.move_player(player, direction)

            if move in ['shoot up', 'shoot down', 'shoot left', 'shoot right']:
                direction = move[6:]
                game.shoot(player, direction)

            if move == 'activate cell' or move == 'e':
                game.activate_cell(player)

            if game.labyrinth.cells[game.players[player].position].content == 'river':
                game.river_move_player(player)

            game.game_over, reason = game.is_game_over()
            if game.game_over:
                print(reason)
                break

        if not game.game_over: game.turn += 1

    print('\nLabyrinth: finished in {} turns.'.format(game.turn))
    game.labyrinth.display_labyrinth()
    game.labyrinth.display_legend()


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


def get_options():
    """ Get options from the user.

    Return a dictionary of the options with keys with bool values.
    """
    choice = 'no'
    while choice not in ['y', 'yes']:
        options = {'wormhole': False, 'river': False, 'bear': False, 'hospital': False}
        answers = input('Enter the name of the options you want separated by a comma, or all: ').lower()

        if answers.strip() == '':
            print('You have chosen no options.')

        elif answers.strip()== 'all':
            options_string = ''
            for opt in options:
                options[opt] = True
                options_string += opt + ', '
            options_string = options_string[:-2]
            print('You have chosen the options: ' + options_string)

        else:
            answers = answers.split(',')

            for i in range(len(answers)):
                answers[i] = answers[i].strip()
                if answers[i][-1] == 's': answers[i] = answers[i][:-1]

            for ans in answers:
                if ans in options.keys(): options[ans] = True

            options_string = ''
            for opt, is_demanded in options.items():
                if is_demanded: options_string += opt + ', '
            if options_string == '': print('You have chosen no options (if not, make sure to write them correctly).')
            else:
                options_string = options_string[:-2]
                print('You have chosen the options: ' + options_string)

        choice = input('Is this correct? [y/n] ').lower().strip()

    if options == '': return None
    return options


def get_player_move(player):
    """ Get player move via the user.

    The move must be one of the known moves.
    """
    known_moves = ['move up', 'move down', 'move left', 'move right', 'w', 's', 'a', 'd',
                   'shoot up', 'shoot down', 'shoot left', 'shoot right',
                   'activate cell', 'e',
                   'exit',
                   'skip']
    move = input(player + ': ').lower()
    while move not in known_moves: move = input('Command unkown.\n' + player + ': ').lower()
    
    return move


if __name__ == '__main__':

    # To display 3 different size labyrinth uncomment below and run main.py
    #for i in range(3): Labyrinth(4 + 4 * i, options={'wormhole': True}).display_labyrinth()
    #exit(0)

    new_game = True
    while new_game:

        play_game_labyrinth()
        answer = input('\nDo you want to play another game? [y/n] ').strip().lower()
        if answer not in ['y', 'yes']: new_game = False