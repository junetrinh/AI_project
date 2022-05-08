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
            print_board(board.size, board.f_board)
            state = State(board, "blue")
            res= state.goal_test("blue")
            print("here")
            minimax = state.result_action("red")
            print("here")
            print(minimax)
            # state_space = State_space(start_state, board, goal_state, False)
            # state_space.a_star_search()

    except IndexError:
        print("usage: python3 -m search path/to/input.json", file=sys.stderr)
        sys.exit(1)



main()