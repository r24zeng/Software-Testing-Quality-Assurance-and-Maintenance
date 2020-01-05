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

import unittest
import wlang.ast as ast
import wlang.sym
import z3

class new_StateVisitor(wlang.sym.SymState):
    def __init__ (self):
        super (new_StateVisitor, self).__init__ ()

class new_ExecVisitor(wlang.sym.SymExec):
    def __init__(self, loop_bound=10):
        super(new_ExecVisitor, self).__init__()


class TestSym (unittest.TestCase):
    def test_one (self):
        prg1 = "havoc x; assume x > 10; assert x > 15"
        ast1 = ast.parse_string (prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        out = [s for s in sym.run (ast1, st)]
        self.assertEquals (len(out), 1)

    def test_two(self):
        # test if-then-else
        prg1 = "havoc x, y, z; if z > y or z >= x then x := x + 1 else x := x-1"
        ast1 = ast.parse_string (prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        out = [s for s in sym.run (ast1, st)]
        self.assertEquals (len(out), 2)

    def test_three(self):
        # test if-then-skip
        prg1 = "havoc x, y, z; if x < y and x <= z then skip; if x = 1 then skip else x := 2; if true then skip; if not false then skip"
        ast1 = ast.parse_string (prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        out = [s for s in sym.run (ast1, st)]
        self.assertEquals (len(out), 4)

    def test_four(self):
        # test while_noinv
        prg1 = "havoc x; while x > 2 do x := x - 1; while x <= 2 do x := x + 1; print_state"
        ast1 = ast.parse_string (prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        out = [s for s in sym.run (ast1, st)]
        self.assertEquals (len(out), 20)

    def test_five(self):
        # test while_inv
        prg1 = "havoc x; y := 10; assume x < 0; while x > 2 inv x >= 2 do x := 1; while y > 2 inv y < 5 do y := y+1"
        ast1 = ast.parse_string (prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        out = [s for s in sym.run (ast1, st)]
        self.assertEquals (len(out), 0)

    def test_five1(self):
        # test while_inv
        prg1 = "havoc x,y; assume y >= 0; c:= 0; r:= x; while c<y inv c > y  and r = x + c do { r:= r+1; c:= c+1 }; assert r= x+y"
        ast1 = ast.parse_string (prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        out = [s for s in sym.run (ast1, st)]
        self.assertEquals (len(out), 0)

    def test_five2(self):
        # test while_inv
        prg1 = "havoc x,y; assume y >= 0; c:= 0; r:= x; while c<y inv c <= y  and r = x + c do { r:= r+1; c:= c+1 }; assert r= x+y"
        ast1 = ast.parse_string (prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        out = [s for s in sym.run (ast1, st)]
        self.assertEquals (len(out), 1)

    def test_six(self):
        # test AExp
        prg1 = "{x := 1; y := 2}; x := (x/y + y)*x/(y-1); print_state"
        ast1 = ast.parse_string (prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        out = [s for s in sym.run (ast1, st)]
        self.assertEquals (len(out), 1)

    def test_seven(self):
        # test solver
        prg1 = "{x := 1; y := 2}; x := (x + y)*x/y - x; print_state"
        ast1 = ast.parse_string(prg1)
        sym = wlang.sym.SymExec ()
        import z3
        st = wlang.sym.SymState (z3.Solver())
        out = [s for s in sym.run(ast1, st)]
        self.assertEquals(len(out), 1)

    def test_eight(self):
        # test run empty
        prg1 = " x := 1; y := 2; assume x > y ; assume x <= y"
        ast1 = ast.parse_string (prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        out = [s for s in sym.run (ast1, st)]
        self.assertEquals (len(out), 0)

    def test_eight1(self):
        # test run empty
        prg1 = " x := 1; y := 2; assert x <= y; assert x > y"
        ast1 = ast.parse_string (prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        out = [s for s in sym.run (ast1, st)]
        self.assertEquals (len(out), 0)

    def test_nine(self):
        # test pick_concrete
        sl = z3.Solver()
        st = wlang.sym.SymState (sl)
        st.add_pc(z3.BoolVal(False))
        self.assertIsNone(st.pick_concerete())

    def test_ten(self):
        # test is_error(), __repr__(), to_smt2()
        st = new_StateVisitor ()
        st.is_error()
        st.__repr__()
        st.to_smt2()

'''   def test_elven(self):
        # test sysmExcute
        ast1 = ast.parse_string(None)
        st = new_ExecVisitor()
        st.run(self, ast1, state=None)
        out = [s for s in st.run (ast1, st)]
        self.assertEquals (len(out), 0)'''



