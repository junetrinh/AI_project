from priority_queue_ import priority_queue
from util import *
from board import *

class State_space:


    def __init__(self, start_state, board, goal_state, debug_flag = False):
        '''
        # param: ...
            debug_flag: once set to 'True', the state_space will print further STDOUT value
        '''
        self._debug_flag = False #debug_flag <- prevent printing un wanted item

        self._path = []
        self._open_list = priority_queue()
        self._start_state = start_state
        self._goal_state = goal_state
        self._board = board

        # config the key state value
        self._start_state.set_heuristic(self._goal_state)
        self._start_state.set_fn()

        # add the starting node to the open list
        self._open_list.add(0, self._start_state)

        if(self._debug_flag):
            initial_board = filled_board(self._board.b_info, self._board.size) 
            initial_board[(self._start_state.r, self._start_state.q)] = "I"
            initial_board[(self._goal_state.r, self._goal_state.q)] = "G"
            print_board(self._board.size, initial_board)
    
    # Private method
    def _find_best(self):
        node = self._open_list.pop()
        
        if node:
            node = node[1]
        return node
    

    def _back_track(self):
        '''
            retrieve the path that link backward from goal to start_state.
        '''
        back_track = []
        last_state = self._path[-1]
        while last_state.parent:
            last_state = last_state.parent
            back_track.append(last_state)
        return back_track



    # Public method
    def set_debug_flag(bool_):
        '''
            indicate that we want futher info for debuging.
            #param: bool - wherether we want to turn the flag on or off
        '''
        self._debug_flag = bool_



    def add_states(self, next_states):
        for s in next_states:
            self._open_list.add(s.fn, s)


    def a_star_search(self):
        '''
            perform a* search with reopen
        '''
        # the following variable is for debuging
        board_label = 0
        solutionBoard = filled_board(self._board.b_info, self._board.size)

        expanding_state = self._find_best()
        while expanding_state and not expanding_state.goal_test(self._goal_state):
            self._board.f_board[(expanding_state.r, expanding_state.q)] = "x"
            successor_states = expanding_state.explore_next_state_a_star(self._board, self._goal_state)
            self.add_states(successor_states)

            self._path.append(expanding_state)
            expanding_state = self._find_best()
        
        # add the goal to the close list to complete the path if any
        if expanding_state:
            self._path.append(self._goal_state)
            self._goal_state.parent = expanding_state

            valid_path = self._back_track()
            print(len(valid_path))
            for i in valid_path[::-1]:
                solutionBoard[(i.r, i.q)] = board_label
                board_label += 1

                i.print_state_valid()
        else:
            print("0")
            return
            
        # display the solution board -> only when the flag indicate so
        if self._debug_flag:
            solutionBoard[(self._goal_state.r, self._goal_state.q)] = "G"
            print("__SOLUTION:")
            print_board(self._board.size, solutionBoard)
            solutionBoard[(self._goal_state.r, self._goal_state.q)] = "null"
