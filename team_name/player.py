from team_name.state_space import *
from team_name.state import *
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
        self.type = player
        self._board_size = n

        # internal state of the game
        self._board = Board(self._board_size)
        self._state_space = State_space(State(self._board, player), player)

    """
            Called at the beginning of your turn. Based on the current state
        of the game, select an action to play.
            ("STEAL") - a player can steal the token that the other player place last round as their own (swap color)
            ("PLACE", r, q) - the capture + placing token on board
    """
    def action(self):
        move = self._state_space.decide()
        
        return ("PLACE", move[0], move[1])

    
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
        self._state_space.update(player, action)
        
        return