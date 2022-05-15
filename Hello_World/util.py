from numpy import array, roll

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

def z_axes(state):
    return -state[0] - state[1]

def find_manhattan_dist(tokenA, tokenB):

        r_dis = tokenA[0] - tokenB[0]
        q_dis = tokenA[1] - tokenB[1]
        z_dis = z_axes(tokenA) - z_axes(tokenB)

        return int((abs(r_dis) + abs(q_dis) + abs(z_dis)) / 2)