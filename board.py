class Board:

    def __init__(self, size, board_info):
        self.size = size
        self.valid_axes = valid_axes(size)
        self.b_info = board_info
        self.f_board = filled_board(board_info, size)

    def print_board_info(self):
        print(self.b_info)

    def print_filled_board(self):
        print(self.f_board)


def shape_board(board_info):

    shaped_board = {}
    for [name, x, y] in board_info:
        shaped_board[(x, y)] = name
    return shaped_board


def check_valid_axes(r, q, n):

    if (r, q) in valid_axes(n):
        return True
    return False


def valid_axes(n):

    axes_set = set()
    for i in range(0, n):
        for j in range(0, n):
            axes_set.add((i, j))
    return axes_set


def filled_board(board_info, n):
    v_axes = valid_axes(n)
    s_board = board_info
    f_board = {}
    for i in v_axes:
        f_board[i] = "null"  # set all the axes into null

    for i in s_board.keys():
        f_board[i] = s_board[i]
    return f_board
