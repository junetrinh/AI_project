from Hello_World.util import *
from Hello_World.environment import *
class Player:

    def __init__(self, player, board_size):
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
        self._environment = Environment(board_size)
        self._type = player
    

    def terminalCheck(self, state, player):
        """
            Check if an terminal state is cause by the previous move
            In order to save cpy cycle, while checking for connect path, look for

                -> feature: check for longest chain as a result of las tmov3
        """
         # check if there are a connect path
        # since last player make a move, only him can potentially win this turn
        # Since last update: alternate the latestUpdate in away we can retrieve last move of both player
        lastPlay = state.latestUpdate[player]

        # red player connect from lowest n (index 0), vice versa
        dimension = 0 if(player == "red") else 1
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
                        return (True, lowest, highest)
                    
                    # add the node to queue so we can expand it
                    openList.append(adj_coord)
                    closeList.add(adj_coord)

        # we check all reachable token but found no chain
        return (False, lowest, highest)
    

    def evaluate(self, lowest, highest, player, state):
        """
            find the score of the state
        """
        # f1: the longest chain
        if(player == self._type):
            dimension = 0 if(player == "red") else 1
            return math.abs(int(lowest[dimension] - int(highest[dimension])))
        else:
            result = self.terminalCheck(state, self._type)
            dimension = 0 if(self._type == "red") else 1
            return math.abs(int(result[1][dimension] - int(result[2][dimension])))

    
    def minimax(self, state, player, closeList, depth = 0):
        """
            explore all the move that select using our heuristic
            then perform minimax till the end and rate it using our eval

            Return:
                depth == 0 : the action that max would perform
                depth >= 1: the minimax value
        """
        Max = True if self._type == player else False
        opponent = "red" if player == "blue" else "blue"
        lastMove = state.lastMove[player]

        checkResult = self.terminalCheck(state, player)

        if(checkResult[0]):
            return self.evaluate(checkResult[1], checkResult[2], player, state)
        

        validMoves = state.getValidMoves()
        optimalMove = validMoves[0]

        for move in validMoves:

            if(move in closeList):
                continue

            closeList.add(move)

            state.place(move, player)
            minimaxValue = self.minimax(state, opponent, closeList, 1)
            





