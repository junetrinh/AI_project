from team_name.board import *
from random import *
from math import *
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
        
        if(not isForwardOnly and ((r_dist == -1) and (q_dist == -1))) :
            res = True

        if(not isForwardOnly and ((r_dist == 1) and (q_dist == 1))) :
            res = True

        if((r_dist == 1) and (q_dist == -1)):
            return True

        if((r_dist == -1) and (q_dist == 1)):
            return True

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
        """
            i will need to remove the player from state, since state is 
                belong to both player
        """
        self._type = player
        self._board = board

        self._level = {"red":dict(), "blue":dict()}
        for i in range(board.size):
            self._level["red"][i] = []
            self._level["blue"][i] = []
            for j in range(board.size):
                red_coord = (i, j)
                blue_coord = (j, i)

                if (board.f_board[red_coord] == "r"):
                    self._level["red"][i].append(red_coord)
                
                if (board.f_board[blue_coord] == "b"):
                    self._level["blue"][i].append(blue_coord)
        
    def place(self, player, coord):
        """
            This is to keep track of internal state of each layer of each player
        """
        # update the board
        status = self._board.place(player, coord)

        if(status):
            if(player=="red"):
                self._level["red"][coord[0]].append(coord)
            else:
                self._level["blue"][coord[1]].append(coord)
        return status


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

        token_dict = self._level[player]
        last_check = (0,0)
        # the chain wont be successful if there are a level missing
        # if(len(token_dict.keys()) < (self._board.size - 1)):
        #     return (False, last_check)

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
                except IndexError:
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
        f1 = find_manhattan_dist(leaf_token, (leaf_token[0], self._board.size - 1))


        #there are more feature introduce later but for now evaluate only using the manhatan
        return f1
