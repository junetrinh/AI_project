from priority_queue_ import priority_queue
from util import *
from board import *
from random import *

class State_space:


    def __init__(self, board, player, debug_flag = False):
        '''
        # param: ...
            debug_flag: once set to 'True', the state_space will print further STDOUT value
        '''
        self._debug_flag = False #debug_flag <- prevent printing un wanted item
        self._enviroment = board
        self._init_board = board
        # through turn # wwe can know which who turn it is currently
        self._turn = 0
        self._player = player
        self._pools = []

    def update(self, player, action):
        """
            apply the action to the state,
                -> this is after the referee judge the action
        """
        # turn the action into an coordinate that player will be place token into
        # this is base on the format of the action object

        coordinate = (0, 0)

        # add the move into our version of current enviroment
        new_enviroment = self.update(coordinate, player)
        self._turn += 1
    
    def minimax_decision(self):
        list_empty_coord = list(self._enviroment._empty_coord)
        move_coord = list_empty_coord[0]

        # the n move does not need to follow any complex search
        if(self._turn < self._enviroment.size):
            # this will be another different strategy which will

            # for now just select a random valid move on board
            

            move_coord = list_empty_coord[int(len(list_empty_coord) * random())]

        else:
            # perform a minimax

            # compute all the minimax from all the possible move, if it result in a win
            # add it to a potential move
            potential_winner = []
            for( move in list_empty_coord):
                print(move)

        return move_coord

        
    # Public method
    def set_debug_flag(bool_):
        '''
            indicate that we want futher info for debuging.
            #param: bool - wherether we want to turn the flag on or off
        '''
        self._debug_flag = bool_

