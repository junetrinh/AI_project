from numpy import zeros, array, roll, vectorize
class Environment:
    """
        This is data of the board
    """

    def __init__(self, board_size, taken=False):
        """
            complexity of create n^2
        """
        self.board_size = board_size
        self._taken = dict()
        self._available = set()
        # format (n, q)
        self.latestUpdate = {"red":(), "blue":()}
        self._capture = []
        
        for n in range(board_size):
            for q in range(board_size):

                if( taken != False):
                    if((n,q) in taken):
                        self._taken[(n, q)] = taken[(n, q)]
                    else:
                        self._available.add((n, q))
                
                else:
                    self._available.add((n, q))
    
    def getValidMove(self):
        return list(self._available)

    def revertMove(self, lastAction, player):
        """
            using the cached last player action we can revert the application of move in constant time
            since 
                insertion / deletion of an item in dict/ set is ~O(1)
            -> this use in stead of store all copy of state
        """

        self._taken.pop(self.latestUpdate[player])
        self._available.add(self.latestUpdate[player])

        #restore the last action
        self.latestUpdate[player] = lastAction


    def place(self, position, token_label):
        """
            Assume that position adding is valid

            Arguments:
                position - Tuple(n, q)
                token_label - character in ["red", "blue"]
        """
        
        self._available.remove(position)
        self._taken[position] = token_label

        self._checkAdjust4Capture(position)
        self.latestUpdate[token_label] = position 
    
    def steal(self):
        """
            Assume that position is valid
        """
        # add the token of player who stole his/her opponent move
        # steal only occur in first move, so the only token on board is definitely belong to our opponent who we want to steal from
        prev_move = [move for move in self._taken.keys()]
        prev_move = prev_move[0]
        
        self._taken[(prev_move[1], prev_move[0])] = "red" if(self._taken[prev_move] == "blue") else "blue"

        # if the result of stealing opponent move is @ a different coordinate
        if(prev_move != (prev_move[1], prev_move[0])):
            self._available.remove((prev_move[1], prev_move[0]))
            self._taken.pop(prev_move)
            self._available.add(prev_move)

    
    def inside_bounds(self, coord):
        """
        REFERENC: code originate from the referee module
        True iff coord inside board bounds.
        """
        r, q = coord
        return r >= 0 and r < self.board_size and q >= 0 and q < self.board_size


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
            self._capture.append(position)


        return list(captured)

                 
            
    
        
# code that originate from the referee
# Utility function to add two coord tuples
_ADD = lambda a, b: (a[0] + b[0], a[1] + b[1])

# Neighbour hex steps in clockwise order
_HEX_STEPS = array([(1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1)], 
    dtype="i,i")

_CAPTURE_PATTERNS = [[_ADD(n1, n2), n1, n2] 
    for n1, n2 in 
        list(zip(_HEX_STEPS, roll(_HEX_STEPS, 1))) + 
        list(zip(_HEX_STEPS, roll(_HEX_STEPS, 2)))]