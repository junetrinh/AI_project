# from util import *
# from board import *

# class State_space:


#     def __init__(self, start_state, board, goal_state, debug_flag = False):
#         '''
#         # param: ...
#             debug_flag: once set to 'True', the state_space will print further STDOUT value
#         '''
#         self._debug_flag = debug_flag

#         self._path = []
#         self._st
#         self._start_state = start_state
#         self._goal_state = goal_state
#         self._board = board

#         # config the key state value
#         self._start_state.set_heuristic(self._goal_state)
#         self._start_state.set_fn()

#     # Private method
#     def _find_best(self):
#         node = self.state_list.pop()
#         if node:
#             node = node[1]

#         return node
    
#     def _back_track(self):
#         back_track = []
#         last_state = self.path[-1]
#         while last_state.last:
#             last_state = last_state.last
#             back_track.append(last_state)
#         return back_track

#     # Public method
#     def a_star_search(self):
#         expanding_state = 
