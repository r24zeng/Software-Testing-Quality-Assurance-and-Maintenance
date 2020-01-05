# The MIT License (MIT)
# Copyright (c) 2016 Arie Gurfinkel

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from __future__ import print_function

import wlang.ast
import cStringIO
import sys
from numbers import Number
import z3
import pdb
import copy
import string
import random


class SymState(object):
    def __init__(self, solver=None):
        # environment mapping variables to symbolic constants
        self.env = dict()
        # path condition
        self.path = list()
        self._solver = solver
        if self._solver is None:
            self._solver = z3.Solver()

        # true if this is an error state
        self._is_error = False

    def add_pc(self, *exp):
        """Add constraints to the path condition"""
        self.path.extend(exp)
        self._solver.append(exp)

    def is_error(self):
        return self._is_error

    def mk_error(self):
        self._is_error = True

    def is_empty(self):
        """Check whether the current symbolic state has any concrete states"""
        res = self._solver.check()
        return res == z3.unsat

    def pick_concerete(self):
        """Pick a concrete state consistent with the symbolic state.
           Return None if no such state exists"""
        res = self._solver.check()
        if res <> z3.sat:
            return None
        model = self._solver.model()
        import wlang.int
        st = wlang.int.State()
        for (k, v) in self.env.items():
            # print("this is v", v)
            # print("this is v",type(v))
            if not isinstance(v, z3.IntNumRef) and not isinstance(v, int):
                try:
                    value = z3.Int(v)
                    # print("value in Pick concrete", value)
                    st.env[k] = model.eval(value)
                    #print("value: ", st.env[k], "in Pick concrete", model.eval(value))
                    #print("st.env[k] in 77", st.env[k])
                except z3.ArgumentError:
                    st.env[k] = v
            else:
                st.env[k] = v
        return st

    def fork(self):
        """Fork the current state into two identical states that can evolve separately"""
        child = SymState()
        child.env = dict(self.env)
        child.add_pc(*self.path)

        return (self, child)

    def __repr__(self):
        return str(self)

    def to_smt2(self):
        """Returns the current state as an SMT-LIB2 benchmark"""
        return self._solver.to_smt2()

    def __str__(self):
        buf = cStringIO.StringIO()
        for k, v in self.env.iteritems():
            buf.write(str(k))
            buf.write(': ')
            buf.write(str(v))
            buf.write('\n')
        buf.write('pc: ')
        buf.write(str(self.path))
        buf.write('\n')

        return buf.getvalue()


class SymExec(wlang.ast.AstVisitor):
    def __init__(self):
        pass

    def run(self, ast, state):
        ## set things up and
        return self.visit(ast, state=state)

    def visit_IntVar(self, node, *args, **kwargs):
        return kwargs['state'].env[node.name]

    def visit_BoolConst(self, node, *args, **kwargs):
        # print("visit_boolConst",node)
        return z3.BoolVal(node.val)

    def visit_IntConst(self, node, *args, **kwargs):
        return z3.IntVal(node.val)

    def visit_RelExp(self, node, *args, **kwargs):
        lhs = self.visit(node.arg(0), *args, **kwargs)
        rhs = self.visit(node.arg(1), *args, **kwargs)

        st = kwargs['state']
        if node.op == '<=':
            if 'if' in kwargs:
                if isinstance(lhs, int):
                    lhs = z3.IntVal(lhs)
                if not isinstance(lhs, z3.ArithRef):
                    lhs = z3.Int(lhs)

                if isinstance(lhs, z3.IntNumRef) and isinstance(rhs, z3.IntNumRef):
                    # print("two integer branch")
                    return op_long(node.op, lhs, rhs)

                if not isinstance(lhs, z3.IntNumRef):
                    # print("no a integer for lhs")
                    kwargs['state'] = build_rst_lst(node.op, lhs, rhs, st)
                else:
                    # print("a integer for lhs")
                    if not isinstance(rhs, z3.ArithRef):
                        rhs = z3.Int(rhs)
                    kwargs['state'] = build_rst_lst(node.op, lhs, rhs, st)

                kwargs['cond'] = not st.is_empty()
                return kwargs

            if 'while' in kwargs:
                # when lhs = X or Y some symbol
                if not isinstance(lhs, z3.ArithRef) and not isinstance(lhs, int):
                    ## not a instance of z3.Arith
                    lhs = z3.Int(lhs)
                if isinstance(lhs, int):
                    lhs = z3.IntVal(lhs)

                if isinstance(lhs, z3.IntNumRef) and isinstance(rhs, z3.IntNumRef):
                    # print("two integer branch")
                    return op_long(node.op, lhs, rhs)
                if not isinstance(lhs, z3.IntNumRef):
                    # if kwargs['times'] == 0 and not isinstance(lhs, z3.IntNumRef):
                    # the first run the while loop and lhs != Integer
                    kwargs['state'] = build_rst_lst(node.op, lhs, rhs, st)
                    # print("189 state in while", kwargs['state'])

                kwargs['cond'] = not st.is_empty()
                return kwargs
            if 'assert' in kwargs:
                if not isinstance(lhs, z3.ArithRef):
                    lhs = z3.Int(lhs)

                kwargs['state'] = build_rst_lst(node.op, lhs, rhs, st)
                kwargs['cond'] = not st.is_empty()
                return kwargs
            if not isinstance(lhs, z3.ArithRef):
                lhs = z3.Int(lhs)
            st.add_pc(opp(node.op, lhs, rhs))
            kwargs['state'] = st
            kwargs['cond'] = not st.is_empty()
            return kwargs
        if node.op == '<':
            if 'if' in kwargs:
                if isinstance(lhs, int):
                    lhs = z3.IntVal(lhs)
                if not isinstance(lhs, z3.ArithRef):
                    lhs = z3.Int(lhs)

                if isinstance(lhs, z3.IntNumRef) and isinstance(rhs, z3.IntNumRef):
                    # print("two integer branch")
                    return op_long(node.op, lhs, rhs)

                if not isinstance(lhs, z3.IntNumRef):
                    # print("no a integer for lhs")
                    kwargs['state'] = build_rst_lst(node.op, lhs, rhs, st)
                else:
                    # print("a integer for lhs")
                    if not isinstance(rhs, z3.ArithRef):
                        rhs = z3.Int(rhs)
                    kwargs['state'] = build_rst_lst(node.op, lhs, rhs, st)

                kwargs['cond'] = not st.is_empty()
                return kwargs

            if 'while' in kwargs:
                # when lhs = X or Y some symbol
                # print("should not change type lhs",type(lhs))
                if not isinstance(lhs, z3.ArithRef) and not isinstance(lhs, int):
                    ## not a instance of z3.Arith
                    lhs = z3.Int(lhs)
                if isinstance(lhs, int):
                    lhs = z3.IntVal(lhs)

                if isinstance(lhs, z3.IntNumRef) and isinstance(rhs, z3.IntNumRef):
                    # print("two integer branch")
                    return op_long(node.op, lhs, rhs)
                if not isinstance(lhs, z3.IntNumRef):
                    # if kwargs['times'] == 0 and not isinstance(lhs, z3.IntNumRef):
                    # the first run the while loop and lhs != Integer
                    kwargs['state'] = build_rst_lst(node.op, lhs, rhs, st)

                kwargs['cond'] = not st.is_empty()
                return kwargs
            if 'assert' in kwargs:
                if not isinstance(lhs, z3.ArithRef):
                    lhs = z3.Int(lhs)

                kwargs['state'] = build_rst_lst(node.op, lhs, rhs, st)
                kwargs['cond'] = not st.is_empty()
                return kwargs
            if not isinstance(lhs, z3.ArithRef):
                lhs = z3.Int(lhs)
            st.add_pc(opp(node.op, lhs, rhs))
            kwargs['state'] = st
            kwargs['cond'] = not st.is_empty()
            return kwargs

        if node.op == '=':
            # if isinstance(lhs, unicode) or isinstance(lhs, z3.ArithRef):
            #     #Above judge is lhs is a symbol or lhs is a expression can be valued in z3
            if 'if' in kwargs:
                if isinstance(lhs, int):
                    lhs = z3.IntVal(lhs)
                if not isinstance(lhs, z3.ArithRef):
                    lhs = z3.Int(lhs)

                if isinstance(lhs, z3.IntNumRef) and isinstance(rhs, z3.IntNumRef):
                    # print("two integer branch")
                    return op_long(node.op, lhs, rhs)

                if not isinstance(lhs, z3.IntNumRef):
                    # print("no a integer for lhs")
                    kwargs['state'] = build_rst_lst(node.op, lhs, rhs, st)
                else:
                    # print("a integer for lhs")
                    if not isinstance(rhs, z3.ArithRef):
                        rhs = z3.Int(rhs)
                    kwargs['state'] = build_rst_lst(node.op, lhs, rhs, st)

                kwargs['cond'] = not st.is_empty()
                return kwargs

            if 'while' in kwargs:
                # when lhs = X or Y some symbol
                if not isinstance(lhs, z3.ArithRef) and not isinstance(lhs, int):
                    ## not a instance of z3.Arith
                    lhs = z3.Int(lhs)
                if isinstance(lhs, int):
                    lhs = z3.IntVal(lhs)

                if isinstance(lhs, z3.IntNumRef) and isinstance(rhs, z3.IntNumRef):
                    # print("two integer branch")
                    return op_long(node.op, lhs, rhs)
                if not isinstance(lhs, z3.IntNumRef):
                    # if kwargs['times'] == 0 and not isinstance(lhs, z3.IntNumRef):
                    # the first run the while loop and lhs != Integer
                    kwargs['state'] = build_rst_lst(node.op, lhs, rhs, st)
                    # print("189 state in while", kwargs['state'])

                kwargs['cond'] = not st.is_empty()
                return kwargs
            if 'assert' in kwargs:
                if not isinstance(lhs, z3.ArithRef):
                    lhs = z3.Int(lhs)

                kwargs['state'] = build_rst_lst(node.op, lhs, rhs, st)
                kwargs['cond'] = not st.is_empty()
                return kwargs
            if not isinstance(lhs, z3.ArithRef):
                lhs = z3.Int(lhs)
            st.add_pc(opp(node.op, lhs, rhs))
            kwargs['state'] = st
            kwargs['cond'] = not st.is_empty()
            return kwargs

        if node.op == '>=':
            if 'if' in kwargs:
                if isinstance(lhs, int):
                    lhs = z3.IntVal(lhs)
                if not isinstance(lhs, z3.ArithRef):
                    lhs = z3.Int(lhs)

                if isinstance(lhs, z3.IntNumRef) and isinstance(rhs, z3.IntNumRef):
                    # print("two integer branch")
                    return op_long(node.op, lhs, rhs)

                if not isinstance(lhs, z3.IntNumRef):
                    # print("no a integer for lhs")
                    kwargs['state'] = build_rst_lst(node.op, lhs, rhs, st)
                else:
                    # print("a integer for lhs")
                    if not isinstance(rhs, z3.ArithRef):
                        rhs = z3.Int(rhs)
                    kwargs['state'] = build_rst_lst(node.op, lhs, rhs, st)

                kwargs['cond'] = not st.is_empty()
                return kwargs

            if 'while' in kwargs:
                # when lhs = X or Y some symbol
                if not isinstance(lhs, z3.ArithRef) and not isinstance(lhs, int):
                    ## not a instance of z3.Arith
                    lhs = z3.Int(lhs)
                if isinstance(lhs, int):
                    lhs = z3.IntVal(lhs)

                if isinstance(lhs, z3.IntNumRef) and isinstance(rhs, z3.IntNumRef):
                    # print("two integer branch")
                    return op_long(node.op, lhs, rhs)
                if not isinstance(lhs, z3.IntNumRef):
                    # if kwargs['times'] == 0 and not isinstance(lhs, z3.IntNumRef):
                    # the first run the while loop and lhs != Integer
                    kwargs['state'] = build_rst_lst(node.op, lhs, rhs, st)

                kwargs['cond'] = not st.is_empty()
                return kwargs
            if 'assert' in kwargs:
                if not isinstance(lhs, z3.ArithRef):
                    lhs = z3.Int(lhs)

                kwargs['state'] = build_rst_lst(node.op, lhs, rhs, st)
                kwargs['cond'] = not st.is_empty()
                return kwargs
            if not isinstance(lhs, z3.ArithRef):
                lhs = z3.Int(lhs)
            st.add_pc(opp(node.op, lhs, rhs))
            kwargs['state'] = st
            kwargs['cond'] = not st.is_empty()
            return kwargs

        if node.op == '>':
            if 'if' in kwargs:
                if isinstance(lhs, int):
                    lhs = z3.IntVal(lhs)
                if not isinstance(lhs, z3.ArithRef):
                    lhs = z3.Int(lhs)

                if isinstance(lhs, z3.IntNumRef) and isinstance(rhs, z3.IntNumRef):
                    # print("two integer branch")
                    return op_long(node.op, lhs, rhs)

                if not isinstance(lhs, z3.IntNumRef):
                    # print("no a integer for lhs")
                    kwargs['state'] = build_rst_lst(node.op, lhs, rhs, st)
                else:
                    # print("a integer for lhs")
                    if not isinstance(rhs, z3.ArithRef):
                        rhs = z3.Int(rhs)
                    kwargs['state'] = build_rst_lst(node.op, lhs, rhs, st)

                kwargs['cond'] = not st.is_empty()
                return kwargs

            if 'while' in kwargs:
                # when lhs = X or Y some symbol
                # print("should not change type lhs",type(lhs))
                if not isinstance(lhs, z3.ArithRef) and not isinstance(lhs, int):
                    ## not a instance of z3.Arith
                    lhs = z3.Int(lhs)
                if isinstance(lhs, int):
                    lhs = z3.IntVal(lhs)

                if isinstance(lhs, z3.IntNumRef) and isinstance(rhs, z3.IntNumRef):
                    # print("two integer branch")
                    return op_long(node.op, lhs, rhs)
                if not isinstance(lhs, z3.IntNumRef):
                    # if kwargs['times'] == 0 and not isinstance(lhs, z3.IntNumRef):
                    # the first run the while loop and lhs != Integer
                    kwargs['state'] = build_rst_lst(node.op, lhs, rhs, st)

                kwargs['cond'] = not st.is_empty()
                return kwargs
            if 'assert' in kwargs:
                if not isinstance(lhs, z3.ArithRef):
                    lhs = z3.Int(lhs)

                kwargs['state'] = build_rst_lst(node.op, lhs, rhs, st)
                kwargs['cond'] = not st.is_empty()
                return kwargs
            if not isinstance(lhs, z3.ArithRef):
                lhs = z3.Int(lhs)
            st.add_pc(opp(node.op, lhs, rhs))
            kwargs['state'] = st
            kwargs['cond'] = not st.is_empty()
            return kwargs

    def visit_BExp(self, node, *args, **kwargs):
        # print("Boolean expression",node)
        kids = [self.visit(a, *args, **kwargs) for a in node.args]

        if node.op == 'not':
            assert node.is_unary()
            assert len(kids) == 1
            return not kids[0]

        fn = None
        base = None
        if node.op == 'and':
            fn = lambda x, y: x and y
            base = True
        elif node.op == 'or':
            fn = lambda x, y: x or y
            base = False

        assert fn is not None
        return reduce(fn, kids, base)

    def visit_AExp(self, node, *args, **kwargs):
        # print("vAexp")
        # print(node.args)
        kids = [self.visit(a, *args, **kwargs) for a in node.args]
        bool = True

        def for_map(kid):
            if isinstance(kid, z3.IntNumRef):
                return kid.as_long()
            elif not isinstance(kid, z3.ArithRef) and not isinstance(kid, int):
                return z3.Int(kid)
            else:
                return kid

        # in order to satisfiy the 10-3=7 operation
        new_kids = map(for_map, kids)

        # if isinstance(new_kids[0], unicode):
        # new_kids[0] = z3.Int(new_kids[0])

        fn = None
        base = None

        if node.op == '+':
            fn = lambda x, y: x + y

        elif node.op == '-':
            fn = lambda x, y: x - y

        elif node.op == '*':
            fn = lambda x, y: x * y

        elif node.op == '/':
            fn = lambda x, y: x / y

        assert fn is not None
        return reduce(fn, new_kids)

    def visit_SkipStmt(self, node, *args, **kwargs):
        return kwargs['state']

    def visit_PrintStateStmt(self, node, *args, **kwargs):
        return kwargs['state']

    def visit_AsgnStmt(self, node, *args, **kwargs):
        st = kwargs['state']
        st.env[node.lhs.name] = self.visit(node.rhs, *args, **kwargs)
        return st

    def visit_IfStmt(self, node, *args, **kwargs):
        kwargs['if'] = 1

        cond = self.visit(node.cond, *args, **kwargs)
        del kwargs['if']
        if isinstance(cond, z3.BoolRef) or isinstance(cond, bool):
            if cond:
                return self.visit(node.then_stmt, *args, **kwargs)
            else:
                if node.has_else():
                    return self.visit(node.else_stmt, *args, **kwargs)
                else:
                    return kwargs['state']

        lstate = []

        kwargs['state'] = cond['state'][0]
        self.visit(node.then_stmt, *args, **kwargs)
        lstate.append(kwargs['state'])
        kwargs['state'] = cond['state'][1]
        if node.has_else():
            self.visit(node.else_stmt, *args, **kwargs)
        lstate.append(kwargs['state'])
        # del kwargs['if']
        return lstate

    def visit_WhileStmt(self, node, *args, **kwargs):
        kwargs['while'] = 1

        if not 'times' in kwargs:
            kwargs['times'] = 0

        d = self.visit(node.cond, *args, **kwargs)

        if isinstance(d, z3.BoolRef) or isinstance(d, bool):
            # print("this case is the normal interpret")
            if d:
                st = self.visit(node.body, *args, **kwargs)
                # execute the loop again

                if isinstance(st, list):
                    kwargs['state'] = st[0]
                return self.visit(node, *args, **kwargs)
            else:
                # loop condition is false, don't execute the body
                return kwargs['state']

        if d['cond'] == True and kwargs['times'] < 10:
            kwargs = d
            if isinstance(kwargs['state'], list):
                # print("I am in the list state",kwargs['state'])
                lstate = copy.deepcopy(kwargs['state'])
                kwargs['state'] = kwargs['state'][0]

                st = self.visit(node.body, *args, **kwargs)
                # execute the loop again
                if len(st) == 1:
                    st = st[0]
                kwargs['state'] = st
                kwargs['times'] = kwargs['times'] + 1

                st = self.visit(node, *args, **kwargs)
                if isinstance(lstate, list):
                    # new_list=[]
                    if not isinstance(st, list):
                        st = [st]
                    # new_list.append(st)
                    st.append(lstate[1])
                    return st
                # return st
        else:
            kwargs['state'] = d['state'][1]
            del kwargs['times']
            return kwargs['state']

    def visit_AssertStmt(self, node, *args, **kwargs):
        ## Don't forget to print an error message if an assertion might be violated
        kwargs['assert'] = 1

        cond = self.visit(node.cond, *args, **kwargs)
        del kwargs['assert']

        if not cond['state'][1].is_empty():
            st = cond['state'][1].mk_error()
            print("There is a feasible path but assertion is not passed")
        kwargs['state'] = cond['state'][0]
        if not cond['cond']:
            # check if this state if it is feasible

            return kwargs['state']

        return kwargs['state']

    def visit_AssumeStmt(self, node, *args, **kwargs):
        cond = self.visit(node.cond, *args, **kwargs)
        return kwargs['state']

    def visit_HavocStmt(self, node, *args, **kwargs):
        st = kwargs['state']
        for v in node.vars:
            ### assign 0 as the default value
            rs = generate_random_Char()
            if rs in st.env.values():
                st.env[v.name] = generate_random_Char()
            else:
                st.env[v.name] = rs

        return st

    def visit_StmtList(self, node, *args, **kwargs):
        st = kwargs['state']
        # print("stmtlist + st: "+str(st))
        kwargs = dict(kwargs)
        prevState = []
        finalState = []
        prevState.append(st)
        for stmt in node.stmts:
            finalState = []
            for state in prevState:
                kwargs['state'] = state
                st_list = self.visit(stmt, *args, **kwargs)
                if not isinstance(st_list, list):
                    st_list = [st_list]
                finalState = finalState + st_list
            prevState = finalState

        st = prevState

        list_new_state = []

        for out in st:
            if not out is None:
                # print("not out.pick_concerete() == None",not out.pick_concerete() == None)
                if not out.pick_concerete() == None and not out.is_empty() and not out.is_error():
                    smt2 = out.to_smt2()
                    list_new_state.append(out)

        return list_new_state


def generate_random_Char():
    return random.choice(string.letters)


def build_rst_lst(op, lhs, rhs, st):
    lst = st
    rst = st.fork()[1]

    lst.add_pc(opp(op, lhs, rhs))
    rst.add_pc(op_opposite(op, lhs, rhs))
    lstate = []
    lstate.append(lst)
    lstate.append(rst)
    return lstate


def opp(op, lhs, rhs):
    if op == '<=':
        return lhs <= rhs
    elif op == '<':
        return lhs < rhs
    elif op == '>':
        return lhs > rhs
    elif op == '>=':
        return lhs >= rhs
    else:
        return lhs == rhs


def op_opposite(op, lhs, rhs):
    if op == '<=':
        return lhs > rhs
    elif op == '<':
        return lhs >= rhs
    elif op == '>':
        return lhs <= rhs
    elif op == '>=':
        return lhs < rhs
    else:
        return lhs != rhs


def op_long(op, lhs, rhs):
    if op == '<=':
        return lhs.as_long() <= rhs.as_long()
    elif op == '<':
        return lhs.as_long() < rhs.as_long()
    elif op == '>':
        return lhs.as_long() > rhs.as_long()
    elif op == '>=':
        return lhs.as_long() >= rhs.as_long()
    else:
        return lhs.as_long() == rhs.as_long()


def _parse_args():    # pragma: no cover
    import argparse
    ap = argparse.ArgumentParser(prog='sym',
                                 description='WLang Interpreter')
    ap.add_argument('in_file', metavar='FILE', help='WLang program to interpret')
    args = ap.parse_args()
    return args


def main():     # pragma: no cover
    args = _parse_args()
    ast = wlang.ast.parse_file(args.in_file)
    st = SymState()
    sym = SymExec()

    states = sym.run(ast, st)
    if states is None:
        print('[symexec]: no output states')
    else:
        count = 0
        for out in states:
            count = count + 1
            print('[symexec]: symbolic state reached')
            print(out)
        print('[symexec]: found', count, 'symbolic states')
    return 0


if __name__ == '__main__':     # pragma: no cover
    sys.exit(main())

