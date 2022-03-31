from util import *
from board import *
from priority_queue_ import *

class State_space:

    def __init__(self, start_state, board, goal_state):
        start_state.set_heuristic(goal_state)
        start_state.set_fn()

        self.state_list = priority_queue()
        self.state_list.add(0, start_state)
        # self.state_list = [start_state]
        self.board = board
        self.goal_state = goal_state
        self.path = []

    

    def add_states(self, next_states):
        for s in next_states:
            self.state_list.add(s.fn, s)
        print("--")
        


    def print_state_space(self):
        for i in self.state_list:
            i.print_state_info()


    def print_path(self):
        for i in self.path:
            i.print_state_valid()

    def back_tracking(self):
        back_track = []
        last_state = self.path[-1]
        while last_state.last:
            last_state = last_state.last
            back_track.append(last_state)
        return back_track


    def a_star_search(self):
        board_label = 0

        expanding_state = self.find_best_a_star()
        expanding_state.print_state_info()
        
        while expanding_state and not expanding_state.goal_test(self.goal_state):
            print("a")
            successors_state = expanding_state.explore_next_state_a_star(self.board, self.goal_state)
            print("b")
            self.add_states(successors_state)
            print("c")
            # if (self.state_list.get_len() > 9999):
            #     print("out of mem")
            #     return 
            self.path.append(expanding_state)
           
            # draw board
            # print("\n\n\n----DRAW BOARD ----")
            # self.board.f_board[(expanding_state.r, expanding_state.q)] = str(board_label)
            # board_label += 1
            # self.board.f_board[(self.goal_state.r, self.goal_state.q)] = "G"
            # print_board(self.board.size, self.board.f_board)
            # self.board.f_board[(self.goal_state.r, self.goal_state.q)] = "null"

            expanding_state = self.find_best_a_star()
            expanding_state.print_state_info()

        self.path.append(self.goal_state)
        self.goal_state.last = expanding_state

        valid_path = self.back_tracking()
        print(len(valid_path))
        solutionBoard = filled_board(self.board.b_info, self.board.size)
        board_label = 0

        for i in valid_path[::-1]:
            solutionBoard[(i.r, i.q)] = board_label
            board_label += 1

            i.print_state_valid()


        solutionBoard[(self.goal_state.r, self.goal_state.q)] = "G"
        print("__SOLUTION:")
        print_board(self.board.size, solutionBoard)

    def check_in_next_list(self, state):
        for i in self.state_list:
            if state.is_equal(i):
                return state
        return False


    def find_best_a_star(self):
        node = self.state_list.pop()
        if node:
            node = node[1]

        return node

    def print_state_list(self):
        for i in self.state_list:
            i.print_state_info()