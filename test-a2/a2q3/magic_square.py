'''Magic Square

https://en.wikipedia.org/wiki/Magic_square

A magic square is a n * n square grid filled with distinct positive integers in
the range 1, 2, ..., n^2 such that each cell contains a different integer and
the sum of the integers in each row, column, and diagonal is equal.

'''

from z3 import *


def solve_magic_square(n, r, c, val):
    solver = Solver()

    ### CREATE CONSTRAINTS AND LOAD STORE THEM IN THE SOLVER
    # initialize and give constrains to every element in magic square
    def constrain_everyone(x1, y1, sl):
        item = BitVec('x%dy%d' % (x1, y1), 32)
        sl.add(item > 0, item <= n**2)
        return item

    # create matrix contains all elements in magic square
    m = [[constrain_everyone(x, y, solver) for x in range(n)] for y in range(n)]

    # add constrains follow sum rule
    s = n*(n**2+1)/2
    for i in range(n):
       # s.add(Sum(matrix[i]) == magic, Sum(column(matrix, i)) == magic)
        solver.add(Sum(m[i]) == s)
        solver.add(Sum([m[j][i] for j in range(n)]) == s)
    solver.add(Sum([m[i][j] for j in range(n) for i in range(n) if i == j]) == s)
    solver.add(Sum([m[i][j] for j in range(n) for i in range(n) if i == n-j-1]) == s)

    # add constrains for non-repeat and fix value
    solver.add(Distinct([m[i][j] for i in range(n) for j in range(n)]))
    solver.add(m[r][c] == val)

    if solver.check() == sat:
        mod = solver.model()
        #print mod

        ### CREATE RESULT MAGIC SQUARE BASED ON THE MODEL FROM THE SOLVER
        res = [[mod[val].as_long() for val in line] for line in m]
        return res
    else:
        return None


def print_square(square):
    '''
    Prints a magic square as a square on the console
    '''
    n = len(square)

    assert n > 0
    for i in range(n):
        assert len(square[i]) == n

    for i in range(n):
        line = []
        for j in range(n):
            line.append(str(square[i][j]))
        print('\t'.join(line))


def puzzle(n, r, c, val):
    res = solve_magic_square(n, r, c, val)
    if res is None:
        print('No solution!')
    else:
        print('Solution:')
        print_square(res)


if __name__ == '__main__':
    n = 3
    r = 1
    c = 1
    val = 5
    puzzle(n, r, c, val)
