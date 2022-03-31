"""
COMP30024 Artificial Intelligence, Semester 1, 2022
Project Part A: Searching

This script contains the entry point to the program (the code in
`__main__.py` calls `main()`). Your solution starts here!

"""

import sys
import json
from state_space import *
from state import *

def main():
    try:
        with open(sys.argv[1]) as file:

            # deal with input
            data = json.load(file)  # treated as a dictionary
            n = data["n"]
            goal_state = State(data["goal"][0], data["goal"][1])
            start_state = State(data["start"][0], data["start"][1])
            board_info = shape_board(data["board"]) # call shape board into wanted format
            board = Board(n,board_info)

            state_space = State_space(start_state, board, goal_state)
            state_space.a_star_search()

    except IndexError:
        print("usage: python3 -m search path/to/input.json", file=sys.stderr)
        sys.exit(1)

    # TODO:
    # Find and print a solution to the board configuration described
    # by `data`.
    # Why not start by trying to print this configuration out using the
    # `print_board` helper function? (See the `util.py` source code for
    # usage information).

