from Hello_World.player import *
from Hello_World.environment import *
from numpy import zeros, array, roll, vectorize

env = Environment( 9,{
    (0,0):"blue",
    (0,1):"blue",
    (0,2):"blue",
    (0,3):"blue",
    (0,4):"blue",
    (0,5):"blue",
    (0,6):"blue",
    (0,7):"blue",
})
env.place((0,8), "blue")
player = Player("blue", 9)

print(player.terminalCheck(env, 1))

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

for pattern in _CAPTURE_PATTERNS:
    print(pattern)