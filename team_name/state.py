from asyncio.windows_events import NULL
from cmath import inf
from board import *
from util import *
from random import *

debugFlag = False

def check_adjaceny( token_A, token_B, isForwardOnly = True, isBackWardOnly = False, debug = False):
        """
            the tokens are only adjacent if the manhatan distance is 1/-1
            for the forward 
        """
        
        r_dist = token_B[0] - token_A[0]
        q_dist = token_B[1] - token_A[1]
        
        res = False
        if(not isBackWardOnly and ((r_dist == 1) and (q_dist == 0))):
            res = True

        if(not isBackWardOnly and ((r_dist == 0) and (q_dist == 1))):
            res = True

        if(not isForwardOnly and ((r_dist == -1) and (q_dist == 0))) :
            res = True

        if(not isForwardOnly and ((r_dist == 0) and (q_dist == -1))) :
            res = True
        if(debug):
            print("\n----check adj-----------------")
            print(r_dist)
            print(q_dist)
            print(token_A)
            print(token_B)
            print(res)
            print("------------------------\n")
        return res


def z_axes(state):
    return -state[0] - state[1]

def find_manhattan_dist(state, goal_state):

        r_dis = state[0] - goal_state[0]
        q_dis = state[1] - goal_state[1]
        z_dis = z_axes(state) - z_axes(goal_state)

        return int((abs(r_dis) + abs(q_dis) + abs(z_dis)) / 2)

class State:

    def __init__(self, board, player):
        # self.r = r
        # self.q = q
        # self.z = z_axes(self)
        # self.next_states = None
        # self.heuristic = None
        # self.gn = 0
        # self.fn = None
        # self.parent = None
        self._type = player
        self._board = board
        self._parent = None

    

    def goal_test(self, player):
        """ 
            search the board for a connect token from either side of the board
            Red will be from 0r -> nr
            blue will be from 0q -> nq

            Arguments:
                player - String either "red" or "blue" which define their win condition    
        """
        # level i: which of r=0, q=1 does it descript the different layer given player
        level_i ,player_label = 0, "r"
        if player == "blue":
            level_i ,player_label = 1, "b"

        token_dict = {}
        last_check = (0,0)
        # Search board (level by level) -> red: level is define by row, blue: level is define by column
        for i in range(self._board.size):
            found = False
            token_dict[i] = []
            
            for j in range(self._board.size):
                # red side
                coord = (i, j)

                if(player == "blue"):
                    coord = (j, i)
                
                # check if that coordinate in board is ocupied
                if (self._board.f_board[coord] == player_label):
                    found = True 
                    token_dict[i].append(coord)
                    last_check = coord
            
            # a level that does not have any token mean that there wont be a connected chain
            if found == False:
                return (False, last_check)

        if(debugFlag):
            print("==========Goal check:level dict=====")
            print("Board_size:" + str((self._board.size -1)))
            for level in token_dict.keys():
                print(str(level) + ":    " + ', '.join([str(elem) for elem in token_dict[level]]))
            
            print("=====================================")
        #if each level, has at least 1 token, we try to connect them  
        close_list = []
        queue = []
        # this is a BFS 
        # add all root token to the queue
        for token in token_dict[0]:
            queue.append((token, 0))
            
        while(len(queue) > 0):            
            # pop the top of the queue
            examined_token = queue.pop(0)
            #we try to either link side-way (same level) or forward linking
            for potential_level in [0, 1]:
                try:
                    for next_token in token_dict[examined_token[1] + potential_level]:
                    
                        if(check_adjaceny(examined_token[0], next_token) and (not next_token in close_list)):
                            
                            # reach goal level
                            if(next_token[level_i] == (self._board.size - 1)):
                                return (True, )

                            last_check = next_token
                            queue.append((next_token, examined_token[1] + potential_level)) 
                            close_list.append(next_token)
                except IndexError and KeyError:
                    continue            
        return (False, last_check)


   


    def evaluate(self, leaf_token, player):
        #f1:  the manhatan distance from leaf node (last visit)
        #f2: total distance from all other piece
        #f3: the least number of oponent piece the better
        # the value will be the linear weight of all those feature

        # calculate f1:
        goal_coord = (leaf_token[0], self._board.size - 1)
        if(player == "blue"):
            goal_coord = (self._board.size - 1, leaf_token[1])
        f1 = self._board.size - find_manhattan_dist(leaf_token, (leaf_token[0], self._board.size - 1)) + random() * 10


        #there are more feature introduce later but for now evaluate only usine the manhatan
        return f1


    def result_action(self, player):
        """
            obtain all possible action
                keep track of state that result in highest: MAX
                keep track state that is lowest: MIN
        """
        # for empty_coord in board._empty_coord:
        max = ( player, 0)
        min = (player, inf)
        
        
        cached_set = set(self._board._empty_coord)
        # Try out all possible move (we have only option to place token into empty hex)
        for coord in cached_set:
            # after action occur, ensure board is upto date: all capture piece are remove
            if(self._board.place(player, coord)):

                # check if this reach the goal 
                res = self.goal_test(player)
                
                # evaluate and update our min max value
                if(not res[0]):
                    val = self.evaluate(res[1], player)

                    if(val > max[1]):
                        max = (res[1], val) 
                    if(val < min[1]):
                        min =(res[1], val)
        return (min, max)
