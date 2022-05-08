
class Board:

    def __init__(self, size, board_info, debug_flag = False):
        self.size = size
        self.valid_axes = valid_axes(size)
        self.b_info = board_info
        self.f_board, self._empty_coord = filled_board(board_info, size)
        self._debug_flag = debug_flag

    # def print_board_info(self):
    #     print(self.b_info)

    def print_filled_board(self):
        print(self.f_board)

    def place(self, player, coordinate):
        label = "r"
        if(player == 'blue'):
            label = 'b'
        
        if(self._empty_coord[coordinate]):
            self._empty_coord.remove(coordinate)
            self.f_board[coordinate] = label

    def update(self, coord, player):
        """
            check if a move into coordicate cause any capture
        """
        # from the adjacent of this move, find 2 hex belong to oponent that are adjacent
        adj_list = []
        adj_list.append((coord[0] + 1, coord[1] - 1))
        adj_list.append((coord[0] + 1, coord[1]))
        adj_list.append((coord[0], coord[1] + 1))
        adj_list.append((coord[0] - 1, coord[1] + 1)) 
        adj_list.append((coord[0] - 1, coord[1]))
        adj_list.append((coord[0], coord[1] - 1))

        #for every consecutive index adj_list item check if they r same color
        i = 0
        next_i = 1
        oponent = "r"
        if(player == "red"):
            oponent = "b"
        for _ in range(6):
            
            if((self.f_board[adj_list[i]] == self.f_board[adj_list[next_i]]) and self.f_board[adj_list[next_i]] == oponent):
                # find the common adj coord of the two
                capture_flag = True
                common_adj = []
                all_adj = set()
                for token in [adj_list[i], adj_list[next_i]]:
                    
                    for adj_coord in [(token[0] + 1, token[1] - 1), (token[0] + 1, token[1]), (token[0], token[1] + 1),
                            (token[0] - 1, token[1] + 1), (token[0] - 1, token[1]), (token[0], token[1] - 1)]:
                        
                        if( (adj_coord not in all_adj) and (adj_coord != adj_list[i] and adj_coord != adj_list[next_i])):
                            all_adj.add(adj_coord)
                        else:
                            common_adj.append(adj_coord)
                    
                common_adj.remove(adj_list[i])
                common_adj.remove(adj_list[next_i])

                # check if both common adj token is of player type, remove the two token
                for token in common_adj:
                    if(self.f_board[token] == oponent or self.f_board[token] == "null"):
                        capture_flag = False
                
                if(capture_flag):
                    
                    self.f_board[adj_list[next_i]] = "null"
                    self.f_board[adj_list[i]] = "null"

                    self._empty_coord.add(adj_list[next_i])
                    self._empty_coord.add(adj_list[i])
            
            i = next_i
            next_i = (next_i + 1) % 6
                    

        

def shape_board(board_info):

    shaped_board = {}
    for [name, x, y] in board_info:
        shaped_board[(x, y)] = name
    return shaped_board


def valid_axes(n):
    axes_set = set()
    for i in range(0, n):
        for j in range(0, n):
            axes_set.add((i, j))
    return axes_set

# we only want to expand unvisit node
def check_close_list(board, state):
    try:
        # if there r none the keyException wil raise and return False
        if(board.f_board[(state.r, state.q)] == "null"):
            return True
    except (KeyError):
        # just to escape the block
        if(board._debug_flag):
            print("Coord: (" + state.r + "," + state.q + ") -> lies outside of the grid" )
    return False

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
