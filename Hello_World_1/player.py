from itertools import accumulate
import math
from os import stat
from turtle import hideturtle
from Hello_World_1.environment import *
import random
from collections import deque
import copy

#reference: originate from reference.py, Neighbour hex steps in clockwise order
_HEX_STEPS = array([(1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1)], 
    dtype="i,i")

# code that originate from the referee
# Utility function to add two coord tuples
_ADD = lambda a, b: (a[0] + b[0], a[1] + b[1])

def z_axes(state):
    return -state[0] - state[1]

def find_manhattan_dist(tokenA, tokenB):

        r_dis = tokenA[0] - tokenB[0]
        q_dis = tokenA[1] - tokenB[1]
        z_dis = z_axes(tokenA) - z_axes(tokenB)

        return int((abs(r_dis) + abs(q_dis) + abs(z_dis)) / 2)
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


    """
            Called at the beginning of your turn. Based on the current state
        of the game, select an action to play.
            ("STEAL") - a player can steal the token that the other player place last round as their own (swap color)
            ("PLACE", r, q) - the capture + placing token on board
    """
    def action(self):
        # for now just select a random move from _available list

        """
            base on current record of the environment, perform an cut-off minimax in order to select 
            an approximate optimal move
        """

        # for the first n move it is just select a random move is sufficient (currently disable)
        if( len(self._environment._taken) < int(4/3 *self._environment.board_size )):
            print("===============HERE===================")
            # if we are blue, we are open to a chance to perform steal
            # check if opponent first move is too powerful ( the closer the move to the centre of board) the more
            # option it leave hence => more powerful
            if(len(self._environment._taken.keys()) == 1 and self._type == "blue"):
                move = self._environment.latestUpdate["red"]
                dimension = 0 if(self._type == "red") else 1

                relativeCentre = (int(self._environment.board_size /2.0) + 1
                            , int(self._environment.board_size /2.0) + 1 )
                # if the move is 2/6 move from the centre, we steal it
                signifDist = int(1.0 /5.0 * self._environment.board_size)
                if(move[0] > (relativeCentre[dimension] - signifDist) 
                    and move[0] < (relativeCentre[dimension] + signifDist) ):
                    return ('STEAL',)
            
            # i need to improve the initial n move strategy instead of random move
            # so i want to start a chain in the middle and try to connect to the the highest level
            dimension = 0 if(self._type == "red") else 1
            # find the exist coord in the first level
            firstNode = (0, (int(self._environment.board_size /2.0) + 1)) if(dimension == 0) else ((int(self._environment.board_size /2.0) + 1), 0)
            for i in range(self._environment.board_size):
                node = (0, i) if (dimension == 0) else (i, 0)

                if(node in self._environment._taken):
                    firstNode = node 
                    print("=============================================================")
                    break
                if(i == self._environment.board_size - 1 ):
                    print("1=============================================================")
                    return ('PLACE', int(node[0]), int(node[1]))
            openList = deque()
            closeList = set()
            # perform BFS from the node expanding out
            # this will aid with the static eval
            lowest = firstNode
            highest = firstNode
            #
            openList.append(firstNode)
            closeList.add(firstNode)
            
            while(len(openList) > 0):
                examinedCoord = openList.popleft()
                # check each coord 1 hex step from exmained cooordinate
                for hex in _HEX_STEPS:

                    adj_coord = _ADD(examinedCoord, hex)
                    # we only care about coord that within the board and of which we have not visit before
                    if(self._environment.inside_bounds(adj_coord) and adj_coord not in closeList):
                        # check if a token with the same value as current player
                        if(adj_coord in self._environment._available
                            or self._environment._taken[adj_coord] != self._type):
                            continue
                        # check if it is either a new lowest layer or highest layer
                        if(adj_coord[dimension] < lowest[dimension]):
                            lowest = adj_coord
                        if(adj_coord[dimension] > highest[dimension]):
                            highest = adj_coord
                        
                        # add the node to queue so we can expand it
                        openList.append(adj_coord)
                        closeList.add(adj_coord)
            # from the highest node try find way to highest
            for hex in _HEX_STEPS:

                adj_coord = _ADD(examinedCoord, hex)
                if(adj_coord[dimension] > highest[dimension]
                    and adj_coord in self._environment._available):
                    return ('PLACE', int(adj_coord[0]), int(adj_coord[1]))
            
        else:
            # we dont want to mess up our environment, so best to make a deep copy once
            state = copy.deepcopy(self._environment)
            closeList = set()
            move =self.minimax(state, int(3* self._environment.board_size), self._type, closeList)
            # # if using heuristic is not enough => for all instance min/opponent is winning
            # # then we will have to expand our option and search all available space
            if(float(move[0]) < 0):
                state = copy.deepcopy(self._environment)
                closeList = set()
                move = self.minimax(state, int(3* self._environment.board_size), self._type, closeList, True)
                
                print(move)
                #if move is still lead to min win, then we might as well play random move
                if(float(move[0]) < 0):
                    print("expand all")
                    valid_move = self._environment.getValidMove()
                    move = valid_move[random.randint(0, len(valid_move) - 1)]
                else:
                    move = move[1]
            else:
                move = move[1]
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
    


    def terminalCheck(self, state, player, depth = 1):
        """
            Check if an terminal state is cause by the previous move
            In order to save cpy cycle, while checking for connect path, look for

                -> feature: check for longest chain as a result of las tmov3
        """
        # reach terminal state if either out of depth or reach goal state
        
        # check if there are a connect path
        # since last player make a move, only him can potentially win this turn
        # Since last update: alternate the latestUpdate in away we can retrieve last move of both player
        lastPlay = state.latestUpdate[player]

        # red player connect from lowest n (index 0), vice versa
        dimension = 0 if(self._type == "red") else 1
        openList = deque()
        closeList = set()
        # perform BFS from the node expanding out
        # this will aid with the static eval
        lowest = lastPlay
        highest = lastPlay
        #
        openList.append(lastPlay)
        closeList.add(lastPlay)
        
        while(len(openList) > 0):
            examinedCoord = openList.popleft()
            # check each coord 1 hex step from exmained cooordinate
            for hex in _HEX_STEPS:

                adj_coord = _ADD(examinedCoord, hex)
                # we only care about coord that within the board and of which we have not visit before
                if(state.inside_bounds(adj_coord) and adj_coord not in closeList):
                    # check if a token with the same value as current player
                    if(adj_coord in state._available
                        or state._taken[adj_coord] != player):
                        continue
                    # check if it is either a new lowest layer or highest layer
                    if(adj_coord[dimension] < lowest[dimension]):
                        lowest = adj_coord
                    if(adj_coord[dimension] > highest[dimension]):
                        highest = adj_coord
                    # check for complete chain
                    if(lowest[dimension] == 0 and 
                        highest[dimension] == self._environment.board_size -1):
                        return (True, lowest, highest, dimension)
                    
                    # add the node to queue so we can expand it
                    openList.append(adj_coord)
                    closeList.add(adj_coord)
        if(depth == 0):
            return (True, lowest, highest, dimension)

        # we check all reachable token but found no chain
        return (False, lowest, highest, dimension)

    def eval(self, lowest, highest, dimension, player, state):
        """
            f1: the current result longest chain
            f2: distance from all other opponent from lowest
            f3: n * percantage of coord player hold ( the more coord, the more option) => avoid capture move
            f4: the number of captured piece as a ratio to our #token on board
            f5: we dont want our front tier to come contact to opponent piece as it might lead to capture move for them
        """
        # compute f1: the longest chain of player 
        # check if the lowest, highest is belong to max
        f1 = 0
        maxLowest = lowest
        maxHighest = highest
        if(player == self._type):
            f1 =  math.fabs(int(lowest[dimension]) - int(highest[dimension]))
        else:
            res =  self.terminalCheck(state, self._type)
            maxLowest = res[1]
            maxHighest = res[2]
            f1 =  math.fabs(int(maxLowest[res[3]]) - int(maxHighest[res[3]]))
        
        minLabel = "red" if self._type == "blue" else "blue"
        dist_min = 0
        dist_max = 0
        count = 0
        player_token_count = 0
        for coord in self._environment._taken.keys():
            if(self._environment._taken[coord] == minLabel):
               dist_min += find_manhattan_dist(maxLowest, coord)
               dist_max += find_manhattan_dist(maxHighest, coord)
               count += 1
            else:
                player_token_count += 1
        f2 = (0.3 * (dist_min / float(count)) + (dist_max / float(count)))

        return f1 + f2
        dist_min = 0
        dist_max = 0
        count = 0
        player_token_count = 0
        for coord in self._environment._taken.keys():
            if(self._environment._taken[coord] == player):
               dist_min += find_manhattan_dist(lowest, coord)
               dist_max += find_manhattan_dist(highest, coord)
               count += 1
            else:
                player_token_count += 1
        #:
        opponent_label = "blue" if player == "red" else "red"
        oponentAdj = 0
        for token in [lowest, highest]: 
            coords = [_ADD(token,s) for s in _HEX_STEPS]

            for coord in coords:
                try:
                    if(self._environment._taken[coord] == opponent_label):
                        oponentAdj+= 1
                except KeyError:
                    continue

        return math.fabs(int(lowest[dimension]) - int(highest[dimension])) \
                    +(0.3 * (dist_min / float(count)) + (dist_max / float(count)))\
                    +(3 * (player_token_count / (self._environment.board_size))) \
                    +(5 * (len(self._environment._capture)/ player_token_count)) \
                    -(3 * (oponentAdj/ 16.0))

    def minimax(self, state, depth, player, closeList, searchAll = False):
        """
            explore all the move that select using our heuristic
            then perform minimax till the end and rate it using our eval
        """
        Min = False if self._type == player else True 
        opponentType = "red" if player == "blue" else "blue"
        # result can either be
        #   (False, Lowest:Tuple(n:int, q:int), Highest: Tuple(n, q), dimension) -> not complete
        #   (True,) -> complete
        lastAction = state.latestUpdate[player]
        result = self.terminalCheck(state, player, depth)

        if(result[0]):
            # if return from out of depth, would be in format (True, Lowest:Tuple(n:int, q:int), Highest=: Tuple(n, q), dimension)
            # else it would be (True)
            # -> return (value, move)
            # @win state
            return (self.eval(result[1], result[2], result[3], player, state), lastAction) if player == self._type else (-self.eval(result[1], result[2], result[3], player, state), lastAction)

        # going through the heuristic favour potential move out of all possible move
        # adjacent node of the lowest -> aggressive strategy to expand our lead
        # adjacent node of the lowest
        # adjacent node of opponent move -> the potentially be defensive/ offensive that threaten a capture
        # a random move that might lead to more opportunity
        # max of 6 + 6 + 6  + 1 growth rate
        valid_move = self._environment.getValidMove()
        randMove = valid_move[random.randint(0, len(valid_move) - 1)]
        value = (self.eval(result[1], result[2], result[3], player, state), randMove) if Min else (-self.eval(result[1], result[2], result[3], player, state),randMove)

        if(searchAll):
            potentialList = list(state._available)
        else:
            potentialList = [result[1], result[2], self._environment.latestUpdate[opponentType], randMove]

        for hex in _HEX_STEPS:
            for examinedToken in potentialList:

                adj_coord = _ADD(examinedToken, hex)
                # ensure we dont revert
                if(adj_coord in self._environment._taken):
                    continue
                if(adj_coord in closeList):
                    continue
                
                if(adj_coord in state._taken):
                    continue

                if (not state.inside_bounds(adj_coord)):
                    # lie out side board
                    continue
                # apply the action to state
                
                cachedLastAction = self._environment.latestUpdate[player]

                closeList.add(adj_coord)
                state.place(adj_coord, player)
                routeMinimax = self.minimax(state, depth - 1, opponentType, closeList, searchAll)

                # restore state to this point
                try:
                    state.revertMove(cachedLastAction, player)
                except KeyError:
                    pass
                if(Min):
                    if(float(routeMinimax[0]) < float(value[0])):
                        value = routeMinimax
                else: # max turn
                    if(float(routeMinimax[0]) > float(value[0])):
                        value = routeMinimax
         
        return value