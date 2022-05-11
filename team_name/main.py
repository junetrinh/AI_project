"""
COMP30024 Artificial Intelligence, Semester 1, 2022
Project Part A: Searching

This script contains the entry point to the program (the code in
`__main__.py` calls `main()`). Your solution starts here!

"""

import sys
import json

from team_name.state_space import *
from team_name.state import *
from team_name.state_space import *
from team_name.util import *
import copy

def main():
    try:
        with open(sys.argv[1]) as file:
            # deal with input
            data = json.load(file)  # treated as a dictionary
            n = data["n"]
            board_info = shape_board(data["board"]) # call shape board into wanted format
            board = Board(n,board_info)
            
            print_board(board.size, board.f_board)
            # state = State(board, "blue")
            # space = State_space(state, "blue")
            # print(space.decide())
            # state_space = State_space(start_state, board, goal_state, False)
            # state_space.a_star_search()

    except KeyError:
        print("usage: python3 -m search path/to/input.json", file=sys.stderr)
        print("index error")
        sys.exit(1)



main()