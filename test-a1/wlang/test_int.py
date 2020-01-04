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
import wlang.int
import wlang.ast as ast
import wlang.parser as parser
#import StringIO


def interp_process(self, prg1):
    ast1 = ast.parse_string(prg1)
    print(str(ast1))
    print(repr(ast1))
    interp = wlang.int.Interpreter()
    st = wlang.int.State()
    st = interp.run(ast1, st)
    return st

class TestInt (unittest.TestCase):
    def test_one (self):
        prg1 = "x :=10; print_state"
        # test parser
        ast1 = ast.parse_string (prg1)
        interp = wlang.int.Interpreter ()
        st = wlang.int.State ()
        st = interp.run (ast1, st)
        self.assertIsNotNone (st)
        # x is defined
        self.assertIn ('x', st.env)
        # x is 10
        self.assertEquals (st.env['x'], 10)
        # no other variables in the state
        self.assertEquals (len (st.env), 1)


# Start to test int.py
    # test havoc
    def test_havoc(self):
        prg = "havoc x"
        st = interp_process(self, prg)
        self.assertIsNotNone(st)
        self.assertIn('x', st.env)
        self.assertEquals (st.env['x'], 0)
        self.assertEquals(len(st.env), 1)

    # test assignment
    def test_assignment(self):
        prg = "x := 10; y := 20; print_state"
        st = interp_process (self, prg)
        self.assertIsNotNone (st)
        # x, y are defined
        self.assertIn ('x', st.env)
        self.assertIn ('y', st.env)
        # x, y are assigned
        self.assertEquals (st.env['x'], 10)
        self.assertEquals (st.env['y'], 20)
        # no other variables in the state
        self.assertEquals (len(st.env), 2)

    # test AExp
    def test_AExp(self):
        prg = "{a := 6; b :=2}; c1 := a+b; c2 := a-b; c3:= a*b; c4 := a/b; print_state"
        st = interp_process (self, prg)
        self.assertIn ('c1', st.env)
        self.assertIn ('c2', st.env)
        self.assertIn ('c3', st.env)
        self.assertIn ('c4', st.env)
        self.assertEquals (st.env['c1'], 8)
        self.assertEquals (st.env['c2'], 4)
        self.assertEquals (st.env['c3'], 12)
        self.assertEquals (st.env['c4'], 3)
        self.assertEquals (len(st.env), 6)

    # test if, skip
    def test_if(self):
        prg = "if true then flag1 := 1; if false then skip else flag2 :=2; if true then skip else flag3 := 3; print_state"
        st = interp_process (self, prg)
        self.assertIn ('flag1', st.env)
        self.assertIn ('flag2', st.env)
        self.assertNotIn ('flag3', st.env)
        self.assertEquals (st.env['flag1'], 1)
        self.assertEquals (st.env['flag2'], 2)
        self.assertEquals (len(st.env), 2)

    # test RelExp
    def test_RelExp(self):
        prg = "x := 6; y := 2; if x > y then flag1 := 1; if x >= y then flag2 :=2;\
         if x < y then flag3 := 3; if x <= y then flag4 :=4; if x = (y+4) then flag5 := 5print_state"
        st = interp_process (self, prg)
        self.assertIn ('flag1', st.env)
        self.assertIn ('flag2', st.env)
        self.assertIn ('flag5', st.env)
        self.assertNotIn ('flag3', st.env)
        self.assertNotIn ('flag4', st.env)
        self.assertEquals (st.env['flag1'], 1)
        self.assertEquals (st.env['flag2'], 2)
        self.assertEquals (st.env['flag5'], 5)
        self.assertEquals (len(st.env), 5)

    # test BExp
    def test_BExp(self):
        prg = "x := 5; if not (x = 5) then skip else flag1 := 1; if (x> 0) and (x < 10) then flag2 :=2; if (x > 5) or (x < 10) then flag3 :=3; print_state"
        st = interp_process (self, prg)
        self.assertIn ('flag1', st.env)
        self.assertIn ('flag2', st.env)
        self.assertIn ('flag3', st.env)
        self.assertEquals (st.env['flag1'], 1)
        self.assertEquals (st.env['flag2'], 2)
        self.assertEquals (st.env['flag3'], 3)
        self.assertEquals (len(st.env), 4)

    # test while
    def test_while(self):
        prg = "x := 3; y := -3; flag := 0; while x > 0 do {x := x-1; flag := flag +1}; while y>0 do { y := y-1; flag := 66}; print_state"
        st = interp_process (self, prg)
        self.assertEquals (st.env['x'], 0)
        self.assertEquals (st.env['y'], -3)
        self.assertEquals (st.env['flag'], 3)
        self.assertEquals (len(st.env), 3)

    # test assert
    def test_assert(self):
        flag0 = False
        try:
            prg = "x := 1; assert(x < 0); flag := 1; print_state "
            st = interp_process (self, prg)
        except:
            flag0 = True
        self.assertTrue(flag0)
        flag0 = False
        try:
            prg = "x := 1; assert(x > 0); flag := 1; print_state"
            st = interp_process (self, prg)
        except:
            flag0 = True
        self.assertFalse(flag0)

    # test assume
    def test_assume(self):
        flag0 = False
        try:
            prg = "x := -1; assume(x > 0); flag := 1; print_state "
            st = interp_process (self, prg)
        except:
            flag0 = True
        self.assertTrue(flag0)
        flag0 = False
        try:
            prg = "x := -1; assume(x < 0); flag := 1; print_state "
            st = interp_process (self, prg)
        except:
            flag0 = True
        self.assertFalse(flag0)

    # test if _name_ == _mian_



# test ast.py
    # test stmlist
    def test_stmlist2(self):
        prg2 = "x := 1; y := 2"
        ast2 = ast.parse_string(prg2)
  #      print repr(ast2)
        self.assertTrue(ast2 == ast2)

    # test skip
    def test_skip2(self):
        prg2 = "skip"
        ast2 = ast.parse_string(prg2)
        self.assertTrue(ast2 == ast2)

    # test print_state
    def test_print2(self):
        prg2 = "print_state"
        ast2 = ast.parse_string(prg2)
        self.assertTrue(ast2 == ast2)

    # test havoc
    def test_havoc2(self):
        prg2 = "havoc x"
        ast2 = ast.parse_string(prg2)
        self.assertTrue(ast2 == ast2)

    # test assignment
    def test_assgn2(self):
        prg2 = "x := 1"
        ast2 = ast.parse_string(prg2)
        self.assertTrue(ast2 == ast2)

    # test binary argument
    def test_arg_binary(self):
        ast2 = ast.Exp('-', [1,2])
        self.assertTrue(ast2.is_binary())


    # test if
    def test_if2(self):
        prg2 = "{x := -1}; if x > 0 then x := 10 else x:= -10"
        ast2 = ast.parse_string(prg2)
        self.assertTrue(ast2.stmts[1] == ast2.stmts[1])

    # test while
    def test_while2(self):
        prg2 = "{x := 3}; while x > 0 do x := x-1"
        ast2 = ast.parse_string(prg2)
        self.assertTrue(ast2.stmts[1] == ast2.stmts[1])

    # test assert
    def test_assert2(self):
        prg2 = "{x := 5}; assert(x > 0) "
        prg2 = "{x := 5}; assert(x > 0) "
        ast2 = ast.parse_string(prg2)
        ast3 = ast.parse_string(prg2)
        ast2 == ast3;

    # test assume
    def test_assume2(self):
        prg2 = "{x := 5}; assume(x > 0)"
        ast2 = ast.parse_string(prg2)
        self.assertTrue(ast2.stmts[1] == ast2.stmts[1])

    # test const
    def test_const2(self):
        prg2 = "2"
        ast2 = ast.Const(prg2)
        self.assertEqual(ast2.__repr__( ), "\'2\'")
        self.assertEqual(ast2.__str__( ), "2")
        print hash(ast2)

    # test int variable
    def test_InVar2(self):
        prg2 = "x"
        ast2 = ast.IntVar(prg2)
        self.assertEqual(ast2.__repr__( ), "\'x\'")
        self.assertEqual(ast2.__str__( ), "x")
        print hash(ast2)

    # test file
    def test_file2(self):
        ast2 = ast.parse_file('wlang/test1.prg')
        self.assertIsNotNone(ast2)


# test Astvisitor in ast.py
# create a new visitor to visit all functions in AstVisitor
class New_AstVisitor(wlang.ast.AstVisitor):
    def __init__(self):
        super(New_AstVisitor, self).__init__()
        self.vars = 0


    # Stm, Exp, Const are the bases
    def visit_Stmt(self, node, *args, **kwargs):
        pass

    def visit_Exp(self, node, *args, **kwargs):
        pass

    def visit_Const(self, node, *args, **kwargs):
        pass

    def visit_StmtList(self, node, *args, **kwargs):
        for n in node.stmts:
            self.vars += 1

    def visit_AsgnStmt(self, node, *args, **kwargs):
        super(New_AstVisitor, self).visit_AsgnStmt(node, *args, **kwargs)
        self.visit(node.lhs)
        self.visit(node.rhs)
        self.vars += 1


# create test unit to test all AstVisitor
class Test_AstVisitor(unittest.TestCase):

    # test visit_AExp
    def test_IntVar (self):
        prg2 = "x := 1"
        ast2 = ast.parse_string(prg2)
        visitor = New_AstVisitor()
        visitor.visit(ast2)
      # self.assertEquals(visitor.vars, 1)

# test other parts of astvisitor and also WhileLangSemantics

    def test_Skip(self):
        prg2 = "skip"
        ast2 = ast.parse_string(prg2)
        visitor = New_AstVisitor()
        visitor.visit(ast2)
 #       self.assertEquals(visitor.vars, 0)

    def test_Print(self):
        prg2 = "print_state"
        ast2 = ast.parse_string(prg2)
        visitor = New_AstVisitor()
        visitor.visit(ast2)
       # self.assertEquals(visitor.vars, 0)

    def test_Assgn(self):
        prg2 = "x := 10"
        ast2 = ast.parse_string(prg2)
        visitor = New_AstVisitor()
        visitor.visit(ast2)
      #  self.assertEquals(visitor.vars, 1)

    def test_If(self):
        prg2 = "if true then x := 20"
        ast2 = ast.parse_string(prg2)
        visitor = New_AstVisitor()
        visitor.visit(ast2)
       # self.assertEquals(visitor.vars, 0)

    def test_While(self):
        prg2 = "while true do x := 20"
        ast2 = ast.parse_string(prg2)
        visitor = New_AstVisitor()
        visitor.visit(ast2)
       # self.assertEquals(visitor.vars, 0)

    def test_Assert(self):
        prg2 = "assert x > 0"
        ast2 = ast.parse_string(prg2)
        visitor = New_AstVisitor()
        visitor.visit(ast2)

    def test_Assume(self):
        prg2 = " assume x > 0"
        ast2 = ast.parse_string(prg2)
        visitor = New_AstVisitor()
        visitor.visit(ast2)

    def test_Havoc(self):
        prg2 = "havoc x"
        ast2 = ast.parse_string(prg2)
        visitor = New_AstVisitor()
        visitor.visit(ast2)

# test printvisitor
    # test prg==Null
    def test_printnone(self):
        visitor2 = ast.PrintVisitor()

    # test stmlist is none
    def test_printstmlist(self):
        ast2 = ast.StmtList(None)
        visitor2 = ast.PrintVisitor()
        visitor2.visit_StmtList(ast2)

    # test WhileLangSemantics in parser.py

    def test_WhileLangSemantics(self):
        Sem = parser.WhileLangSemantics()
        prg3 = "{x := 1; y :=2}; if x > 0 then y := y+1 else skip"
        ast3 = ast.parse_string(prg3)
        self.assertEquals(Sem.start(ast3), ast3)
        self.assertEquals(Sem.stmt_list(ast3), ast3)
        self.assertEquals(Sem.stmt(ast3), ast3)
        self.assertEquals(Sem.asgn_stmt(ast3), ast3)
        self.assertEquals(Sem.block_stmt(ast3), ast3)
        self.assertEquals(Sem.skip_stmt(ast3), ast3)
        self.assertEquals(Sem.print_state_stmt(ast3), ast3)
        self.assertEquals(Sem.if_stmt(ast3), ast3)
        self.assertEquals(Sem.while_stmt(ast3), ast3)
        self.assertEquals(Sem.assert_stmt(ast3), ast3)
        self.assertEquals(Sem.assume_stmt(ast3), ast3)
        self.assertEquals(Sem.havoc_stmt(ast3), ast3)
        self.assertEquals(Sem.var_list(ast3), ast3)
        self.assertEquals(Sem.bexp(ast3), ast3)
        self.assertEquals(Sem.bterm(ast3), ast3)
        self.assertEquals(Sem.bfactor(ast3), ast3)
        self.assertEquals(Sem.batom(ast3), ast3)
        self.assertEquals(Sem.bool_const(ast3), ast3)
        self.assertEquals(Sem.rexp(ast3), ast3)
        self.assertEquals(Sem.rop(ast3), ast3)
        self.assertEquals(Sem.aexp(ast3), ast3)
        self.assertEquals(Sem.addition(ast3), ast3)
        self.assertEquals(Sem.subtraction(ast3), ast3)
        self.assertEquals(Sem.term(ast3), ast3)
        self.assertEquals(Sem.mult(ast3), ast3)
        self.assertEquals(Sem.division(ast3), ast3)
        self.assertEquals(Sem.factor(ast3), ast3)
        self.assertEquals(Sem.neg_number(ast3), ast3)
        self.assertEquals(Sem.atom(ast3), ast3)
        self.assertEquals(Sem.name(ast3), ast3)
        self.assertEquals(Sem.number(ast3), ast3)
        self.assertEquals(Sem.INT(ast3), ast3)
        self.assertEquals(Sem.NAME(ast3), ast3)
        self.assertEquals(Sem.NEWLINE(ast3), ast3)
