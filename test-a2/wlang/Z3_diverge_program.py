''' ECE653/Assignment 2 Question4
Write my own program takes longer time to run
(e) Provide a program on which your symbolic execution engine diverges (i.e., takes longer than a few seconds to
run).


'''

from z3 import *

def main():
    b, c = Ints('b c')
    a = Array('a', IntSort(), IntSort())
    f = Function('f', IntSort(), IntSort())
    solver = Solver()
    solver.add(c == b + IntVal(2))
    lhs = f(Store(a, b, 3)[c -2])
    rhs = f(c -b + 1)
    solver.add(lhs == rhs)
    res = solver.check()
    if res == sat:
        print 'sat'
        print solver.model()
    elif res == unsat:
        print 'unsat'
    else:
        print 'unknown'

if __name__ == '__main__':
    main()


