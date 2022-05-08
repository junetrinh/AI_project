from board import *
from util import *
class State:

    def __init__(self, board, player):
        """"
            Need ot change this into a board
                -> new state of the game will be the board
        """"
        # self.r = r
        # self.q = q
        # self.z = z_axes(self)
        # self.next_states = None
        # self.heuristic = None
        # self.gn = 0
        # self.fn = None
        # self.parent = None
        self._type = player
        self._board = board
        self._parent = None


    def goal_test(player, goal_state):
        # search the board for a connect token from either side of the board
        # Red will be from 0r -> nr
        # blue will be from 0q -> nq
        main_dimention = r 
        support_dimentaion = q 

        if(player == 'red'){
            token_dict = {}
            # check each level for a token, if a level missing a token then there wont be any connected path
            # while checking compute a diction of token which exist @each level
            for(r in range(self._board.size)){
                found = False
                token_dict[i] =  []
                
                for(q in range(self._board.size)){
                    if(self._board.f_board[(r, q)] == "r"){
                        found = True
                        token_dict[i].append((r, q))
                    }
                }
                if(found == False){
                    return False
                }
            }

            #if each level, has at least 1 token, we try to connect them
            queue = []
            # this is kind of a BFS 
            # add all root token to the queue
            for(token in token_dict[0]){
                queue.append((token, 0))
            }
            examined_token = null
            last_check = null
            while(len(queue) > 0){
                examined_token = queue[0];

                del queue[0];

                for(next_token in token_dict[examined_token[1] + 1]{
                    if(check_adjaceny(examined_token[0], next_token)){
                        # arrived at last layer when the r is equal to the size
                        if(next_token[0] == (self._board.size -1)){
                            return (True, );
                        }
                        last_check = next_token
                        queue.append((next_token, examined_token[1] + 1))
                    }
                })
            }
        }
        
        return (False, last_check)

    def check_adjaceny(token_A, token_B, isForwardOnly = True, isBackWardOnly = False):
        """
            the tokens are only adjacent if the manhatan distance is 1/-1
            for the forward 
        """
        r_dist = token_A[0] - token_B[0]
        q_dist = token_A[1] - token_B[1]
        if(not isBackWardOnly and ((r_dis == 1) and (q_dis == 0))){
            return True
        }

        if(not isBackWardOnly and ((r_dis == 0) and (q_dis == 1))){
            return True
        }

        if(not isForwardOnly and ((r_dis == -1) and (q_dis == 0))) {
            return True
        }

        if(not isForwardOnly and ((r_dis == 0) and (q_dis == -1))) {
            return True
        }
        return False


    def evaluate(self, leaf_token){
        #f1:  the manhatan distance from leaf node (last visit)
        #f2: total distance from all other piece
        #f3: the least number of oponent piece the better
        # the value will be the linear weight of all those feature

        # calculate f1:
        f1 = self._board.size - find_manhattan_dist(leaf_token, (leaf_token[0], self._board.size - 1))


        #calculate f2:
    }

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
    return -state[0] - state[1]


def find_manhattan_dist(state, goal_state):
    r_dis = state[0] - goal_state[0]
    q_dis = state[1] - goal_state[1]
    z_dis = z_axes(state) - z_axes(goal_state)
    return int((abs(r_dis) + abs(q_dis) + abs(z_dis)) / 2)

def check_valid_state(state, board):
    """
        a valid state is one which in the board and the move is not go to coordinate that are occupied
    """
    # if (state.r, state.q) in board.valid_axes:
        # return True
    # return False
    return (state.r >= 0 and state.r <board.size) and (state.q >= 0 and state.q <board.size) and  (board.f_board[(state.r, state.q)] == "null")
