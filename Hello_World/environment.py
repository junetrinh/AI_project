"""
    This unit keep track of the fully observable, sequential environment
"""
from Hello_World.util import *

class Environment:

    def __init__(self, board_size, init_board = False):
        """
            Arguments:

                board_size - Integer
                init_board - dict((n, q): "token_label" in ["red", "blue"])
        """

        self.size = board_size
        
        self._taken = dict()
        self._available = set()
        self._capture = {
            "red": dict(), # (n, q) : [(n,q)]
            "blue": dict()
        }
        
        self.lastMove = {
            "red": (),
            "blue": ()
        }

        # if there are an init board that is not empty add them
        for n in range(self.size):
            for q in range(self.size):

                if(init_board):
                    if((n, q) in init_board):
                        self._taken[(n, q)] = init_board[(n, q)]
                    else:
                        self._available.add((n, q))
    

    def getValidMoves(self):
        return list(self._available)


    def _checkAdjust4Capture(self, lastMove):
        """
            Reference: This code is originate from the referee module
            an update to ensure all token is remove if last action lead to a capture move.
        """
        # reference: code from reference: pre-compile pattern of capture
        # Check each capture pattern intersecting with coord
        opp_type = self._taken[lastMove]
        mid_type = "red" if opp_type == "blue" else "blue"
        captured = set()
        # Check each capture pattern intersecting with coord
        for pattern in _CAPTURE_PATTERNS:
            coords = [_ADD(lastMove, s) for s in pattern]
            
            # No point checking if any coord is outside the board!
            if all(map(self.inside_bounds, coords)):
                try:
                    tokens = [self._taken[coord] for coord in coords]
                    if tokens == [opp_type, mid_type, mid_type]:
                        # Capturing has to be deferred in case of overlaps
                        # Both mid cell tokens should be captured
                        captured.update(coords[1:])
                except KeyError:
                    continue
        for position in captured:
            self._taken.pop(position)
            self._available.add(position)
        
        self._capture[opp_type][lastMove] = captured


        return list(captured)


    def place(self, position, label):
        """
            Assume that position adding is valid

            Arguments:
                position - Tuple(n, q)
                label - character in ["red", "blue"]
        """
        self._available.remove(position)
        self._taken[position] = label
        self._checkAdjust4Capture(position)
        self.lastMove[label] = position

    
    def steal(self):
        """
            steal only occur for second player in their first move (blue)
        """
        # retrieve the first move of red.
        move = self.lastMove["red"]
        stealMove = (move[1], move(0))
        if(move == () or len(self._taken.keys()) != 1):
            # invalid
            return 
        
        self._taken[stealMove] = "blue"

        # clear the old move if appropriate
        if(move != stealMove):
            self._available.remove(stealMove)
            self._taken.pop(move)
            self._available.add(move)
    

    def revertMove(self, lastAction, player):
        """
            using the cached last player action we can revert the application of move in constant time
            since 
                insertion / deletion of an item in dict/ set is ~O(1)
            -> this use in stead of store all copy of state
        """

        self._taken.pop(self.lastMove[player])
        self._available.add(self.lastMove[player])

        # check if last move cause any capture, if so revert
        opponent = "red" if player == "blue" else "blue"
        for captureMove in self._capture[player]:
            if(captureMove == lastAction):
                for capture in self._capture[player][captureMove]:
                    self._available.remove(capture)
                    self._taken[capture] = opponent

                self._capture[player].pop(captureMove)

        #restore the last action
        self.lastMove[player] = lastAction


    def inside_bounds(self, coord):
        """
        REFERENC: code originate from the referee module
        True iff coord inside board bounds.
        """
        r, q = coord
        return r >= 0 and r < self.board_size and q >= 0 and q < self.board_size