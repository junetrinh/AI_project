class Board:

    def __init__(self, size, board_info = {}, debug_flag = False):
        self.size = size
        self.valid_axes = valid_axes(size)
        self.b_info = board_info
        self.f_board, self._empty_coord = filled_board(board_info, size)
        self._debug_flag = debug_flag


    def print_filled_board(self):
        print(self.f_board)


    def place(self, player, coordinate):
        """
            update the board info that if possible
            Arguments:
                player - String either "red" or "blue"
                coordinate - Tuple (r, q) where the potential move could go
            
            Return:
                Bool - indicate if the move is valid
        """
        label = "r"
        if(player == 'blue'):
            label = 'b'
        
        if(coordinate in self._empty_coord):
            self._empty_coord.remove(coordinate)
            self.f_board[coordinate] = label
            # update the board to ensure all capture occur
            self.update(coordinate, player)
            return True 
        
        return False


    def update(self, coord, player):
        """
            check if a move into coordicate cause any capture
        """
        i = 0
        next_i = 1
        oponent = "r"
        if(player == "red"):
            oponent = "b"
        
        # Find all adjcent coordinate
        adj_list = []
        adj_list.append((coord[0] + 1, coord[1] - 1))
        adj_list.append((coord[0] + 1, coord[1]))
        adj_list.append((coord[0], coord[1] + 1))
        adj_list.append((coord[0] - 1, coord[1] + 1)) 
        adj_list.append((coord[0] - 1, coord[1]))
        adj_list.append((coord[0], coord[1] - 1))

        
        # if the coordinate data is differ from expectation, do nothing
        if(self.f_board[coord] == oponent or self.f_board[coord] == "null"):
            #do nothing
            return

        # for each pair of adjacent hex from the coord, check if there are both belong to player's oponent
        for _ in range(6):
            try:
                if((self.f_board[adj_list[i]] == self.f_board[adj_list[next_i]]) and self.f_board[adj_list[next_i]] == oponent):
                    # find the common adj coord of the two
                    capture_flag = True
                    common_adj = []
                    all_adj = set()
                    # try to obtain the 2 hex that would be form a diamond with this 2 adjacent hex
                    for token in [adj_list[i], adj_list[next_i]]:
                        
                        for adj_coord in [(token[0] + 1, token[1] - 1), (token[0] + 1, token[1]), (token[0], token[1] + 1),
                                (token[0] - 1, token[1] + 1), (token[0] - 1, token[1]), (token[0], token[1] - 1)]:
                            
                            if( (adj_coord not in all_adj) and (adj_coord != adj_list[i] and adj_coord != adj_list[next_i])):
                                all_adj.add(adj_coord)
                            else:
                                common_adj.append(adj_coord)
                        
                    common_adj.remove(adj_list[i])
                    common_adj.remove(adj_list[next_i])

                    # check if both of that hex belong to player
                    for token in common_adj:
                       
                        if(self.f_board[token] == oponent or self.f_board[token] == "null"):
                            capture_flag = False
                        
                    # if it is , player will be able to capture their oponent
                    if(capture_flag):
                        self.f_board[adj_list[next_i]] = "null"
                        self.f_board[adj_list[i]] = "null"

                        self._empty_coord.add(adj_list[next_i])
                        self._empty_coord.add(adj_list[i])
            except KeyError:
                i = next_i 
            i = next_i
            next_i = (next_i + 1) % 6
                    

def valid_axes(n):
    axes_set = set()
    for i in range(0, n):
        for j in range(0, n):
            axes_set.add((i, j))
    return axes_set        

def shape_board(board_info):

    shaped_board = {}
    for [name, x, y] in board_info:
        shaped_board[(x, y)] = name
    return shaped_board


def filled_board(board_info, n):
    """
        Does not need the board info any more since the board is should be recycle 
    """
    v_axes = valid_axes(n)
    s_board = board_info
    empty_coord = set()
    f_board = {}
    for i in v_axes:
        f_board[i] = "null"  # set all the axes into null
        empty_coord.add(i)

    for i in s_board.keys():
        f_board[i] = s_board[i]
        empty_coord.remove(i)
    return f_board, empty_coord