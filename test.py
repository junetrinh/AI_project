from Hello_World.player import *
from Hello_World.environment import *
from numpy import zeros, array, roll, vectorize

player = Player("blue", 9)
dictionary = {
        (0,0):"blue",
        (1,1):"red",
        (1,2):"red",
        (0,1):"blue",
        (0,2):"blue",
        (0,3):"blue",
        (0,4):"blue",
        (0,5):"blue",
        (0,6):"blue",
        (0,7):"blue",
        (1,7):"blue",
    }
for move in dictionary.keys():
    player.turn(dictionary[move], ("PLACE", move[0], move[1]))

print(player._environment.latestUpdate)
cloneState = copy.deepcopy(player._environment)
closelist = set()
print(player.minimax(cloneState, 10000, "blue", closelist))

# print(len(env._taken.keys()))
# code that originate from the referee
# Utility function to add two coord tuples
_ADD = lambda a, b: (a[0] + b[0], a[1] + b[1])

# Neighbour hex steps in clockwise order
_HEX_STEPS = array([(1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1)], 
    dtype="i,i")

_CAPTURE_PATTERNS = [[_ADD(n1, n2), n1, n2] 
    for n1, n2 in 
        list(zip(_HEX_STEPS, roll(_HEX_STEPS, 1))) + 
        list(zip(_HEX_STEPS, roll(_HEX_STEPS, 2)))]
