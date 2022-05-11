import math
from team_name.board import *
from random import *
from math import *
from team_name.state import *
import copy
class State_space:


    def __init__(self, state, player, debug_flag = False):
        '''
        # param: ...
            debug_flag: once set to 'True', the state_space will print further STDOUT value
        '''
        self._debug_flag = False #debug_flag <- prevent printing un wanted item
        self._environment = state
        self._init_state = state
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
        if(action[0] == "PLACE"):
            self._environment.place(player, (action[1], action[2]))   

        # add the move into our version of current enviroment
        self._turn += 1

    def check_max(coord, value, max):
        if(value < max):
            return value
        return max

    def check_min(coord, value, min):
        if(value > min):
            return value
        return min
    
    def minimax(self, state, depth, player):
        # print_board(state._board.size, state._board.f_board)
        test_result = state.goal_test(player)
        # print(player)
        if (depth == 0 or test_result[0]):
            # print("end depth" if depth == 0 else "finish")
            # if opponent win: inf, else 0
            if(test_result[0]):
                # print("win")
                if(player == self._player):
                    return 0
                else:
                    # print("player win: " + player )
                    return math.inf
            
            return state.evaluate(test_result[1], player)
        cached_set = list(state._board._empty_coord)
        # return
        # max player
        if(self._player == player):
        
            maxValue = math.inf
            # Try out all possible move (we have only option to place token into empty hex)
            for coord in cached_set:
                clone_state = State(state._board, player)
                # copy.deepcopy(state)
                # after action occur, ensure board is upto date: all capture piece are remove
                if(clone_state.place(player, coord)):
                    value = self.minimax(clone_state, depth - 1, "red" if player == "blue" else "blue")
                    maxValue = self.check_max(value, maxValue)
                
            return maxValue
        else:

            minValue = -math.inf
            # Try out all possible move (we have only option to place token into empty hex)
            for coord in cached_set:
                clone_state = State(state._board, player)
                # clone_state = copy.deepcopy(state)
                # after action occur, ensure board is upto date: all capture piece are remove
                if(clone_state.place(player, coord)):
                    value = self.minimax(clone_state, depth - 1, "red" if player == "blue" else "blue")
                    minValue = self.check_min(value, minValue)
            
            return minValue


    def decide(self):
        list_empty_coord = list(self._environment._board._empty_coord)
  
        move_coord = list_empty_coord[0]
        # print(move_coord)
        # the n move does not need to follow any complex search
        if(False and self._turn < self._environment._board.size):
            
            # this will be another different strategy which will

            # for now just select a random valid move on board
            

            move_coord = list_empty_coord[int(len(list_empty_coord) * random())]

        else:
            # perform a minimax

            # compute all the minimax from all the possible move, if it result in a win
            # add it to a potential move
            minimax_list = []
            # create a clone of environment
            return list_empty_coord[0]
            for move in list_empty_coord:
                clone_env = copy.deepcopy(self._environment)
                clone_env.place(self._player , move)
                # for each possible move find the minimax value of that branch
                minimax_list.append((self.minimax(clone_env, 3, self._player), move))

            # get max
            local_max = math.inf
            for option in minimax_list:
                if(option[0] < local_max):
                    local_max = option[0]
                    move_coord = option[1]
            

        return move_coord

        
    # Public method
    def set_debug_flag(self, bool_):
        '''
            indicate that we want futher info for debuging.
            #param: bool - wherether we want to turn the flag on or off
        '''
        self._debug_flag = bool_

