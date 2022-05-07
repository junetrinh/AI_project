from board import *
from util import *
class State:

    def __init__(self, r, q):
        self.r = r
        self.q = q
        self.z = z_axes(self)
        self.next_states = None
        self.heuristic = None
        self.gn = 0
        self.fn = None
        self.parent = None

    def goal_test(self, goal_state):
        if self.is_equal(goal_state):
            return True
        return False

    def is_equal(self, other_state):
        return self.r == other_state.r and self.q == other_state.q

    def set_heuristic(self, goal_state):
        self.heuristic = find_heuristic(self, goal_state)

    def print_state_info(self):
        print(f"[({self.r}, {self.q}), "
                  f"h: {self.heuristic}, fn: {self.fn}, "
                  f"gn: {self.gn}]")
        if self.parent:
            print(f"\tParent:[({self.parent.r}, {self.parent.q}), "
                  f"h: {self.parent.heuristic}, fn: {self.parent.fn}, "
                  f"gn: {self.parent.gn}]")


    def explore_next_state_a_star(self, board, goal_state):
        new_state_set = set()
        for i in [-1, 1]:
            new_state_r = State(self.r + i, self.q)
            new_state_q = State(self.r, self.q + i)
            new_state_rq = State(self.r + i, self.q - i)

            # generate state for each instance of state result from an action of {move in q, move in r, move diagonal}
            for state_instance in [new_state_r, new_state_q, new_state_rq]:
                if  ( not check_valid_state(state_instance, board)
                    and 
                        not check_close_list(board, state_instance)):
                    continue

                state_instance.set_heuristic(goal_state)
                state_instance.update_gn(self)
                state_instance.set_fn()
                state_instance.parent = self
                new_state_set.add(state_instance)
        
        return list(new_state_set)


    def print_state_valid(self):
        print_coordinate(self.r, self.q)

    def set_fn(self):
        self.fn = self.heuristic + self.gn

    def update_gn(self, parent_state):
        self.gn = parent_state.gn + 1


def z_axes(state):
    return -state.r - state.q


def find_heuristic(state, goal_state):
    r_dis = state.r - goal_state.r
    q_dis = state.q - goal_state.q
    z_dis = state.z - goal_state.z
    return int((abs(r_dis) + abs(q_dis) + abs(z_dis)) / 2)

def check_valid_state(state, board):
    """
        a valid state is one which in the board and the move is not go to coordinate that are occupied
    """
    # if (state.r, state.q) in board.valid_axes:
        # return True
    # return False
    return (state.r >= 0 and state.r <board.size) and (state.q >= 0 and state.q <board.size) and  (board.f_board[(state.r, state.q)] == "null")
