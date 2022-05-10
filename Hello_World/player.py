from Hello_World.environment import *
import random

class Player:

    
    def __init__(self, player, n):
        """
            Called once at the beginning of a game to initialise this player.
        Set up an internal representation of the game state.

            The parameter player is the string "red" if your player will
        play as Red, or the string "blue" if your player will play
        as Blue.

        Arguments:
            player -- String in ["red", :blue"] represent the side + colour of the player
            n -- Integer that is the size of the board being use
        """
        self._environment = Environment(n)
        self._type = player
        print(player)


       # initiate the state of the game

    """
            Called at the beginning of your turn. Based on the current state
        of the game, select an action to play.
            ("STEAL") - a player can steal the token that the other player place last round as their own (swap color)
            ("PLACE", r, q) - the capture + placing token on board
    """
    def action(self):
        # for now just select a random move from _available list

        
        valid_move = self._environment.getValidMove()
        # print(valid_move)
        move = valid_move[random.randint(0, len(valid_move) - 1)]
        if(len(self._environment._taken) == 0 and move == (self._environment.board_size / 2.0, self._environment.board_size / 2.0)):
            move = (2, 1)
        return ('PLACE', int(move[0]), int(move[1]))
    
    """
            Called at the end of each player's turn to inform this player of 
        their chosen action. Update your internal representation of the 
        game state based on this. The parameter action is the chosen 
        action itself. 
        
            Note: At the end of your player's turn, the action parameter is
        the same as what your player returned from the action method
        above. However, the referee has validated it at this point.

        Arguments:
            player -- String in ["red", :blue"] represent the side + colour of the player
            action -- the action of either player label by the "player" attribute
    """
    def turn(self, player, action):
        if(action[0] == "PLACE"):
            self._environment.place((action[1], action[2]), player)
        else:
            self._environment.steal()
        