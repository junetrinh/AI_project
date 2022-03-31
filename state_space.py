from util import *
from board import *

class State_space:

    def __init__(self, start_state, board, goal_state):
        start_state.set_heuristic(goal_state)
        start_state.set_fn()

        self.state_list = [start_state]
        self.board = board
        self.goal_state = goal_state
        self.path = []

    def add_states(self, next_states):
        for i in next_states:
            self.state_list.append(i)


    def find_best(self):
        if (len(self.state_list) <= 0):
            return
        current_state = self.state_list[0]
        current_min = current_state.heuristic
        for i in self.state_list:
            if i.heuristic <= current_min:
                current_min = i.heuristic
                current_state = i
        return current_state

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
        # print the start state
        start_state = self.state_list[0]
        board_label = 0

        # explore the start state
        next_state_to_explore = start_state
        while not next_state_to_explore.goal_test(self.goal_state): # goal test


            next_state_list = next_state_to_explore.explore_next_state_a_star(self.board, self.goal_state)
            self.add_states(next_state_list)
            state_list_len = len(self.state_list)

            if (state_list_len > 9999):
                print("0")
                return

            self.state_list.remove(next_state_to_explore)

            self.path.append(next_state_to_explore)
            self.board.f_board[(next_state_to_explore.r, next_state_to_explore.q)] = str(board_label)
            board_label += 1
            self.board.f_board[(self.goal_state.r, self.goal_state.q)] = "G"
            print_board(self.board.size, self.board.f_board)
            self.board.f_board[(self.goal_state.r, self.goal_state.q)] = "null"

            next_state_to_explore = self.find_best_a_star()
        self.path.append(self.goal_state)
        self.goal_state.last = next_state_to_explore

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
        if (len(self.state_list) <= 0):
            return
        current_state = self.state_list[0]
        current_min = current_state.fn
        for i in self.state_list:
            if i.fn <= current_min:
                current_min = i.fn
                current_state = i
        return current_state

    def print_state_list(self):
        for i in self.state_list:
            i.print_state_info()