import unittest
import wlang.ast as ast
import wlang.stats_visitor as stats_visitor

class TestStatsVisitor (unittest.TestCase):
    def test_one (self):
        prg1 = "x := 10; print_state"
        ast1 = ast.parse_string (prg1)
        print (ast1)
        sv = stats_visitor.StatsVisitor ()
        sv.visit (ast1)
        self.assertEquals(sv.get_num_stmts(), 2)
        self.assertEquals(sv.get_num_vars(),1)
        # UNCOMMENT to run the test
        # self.assertEquals(sv._num_stmts (), 2)
        # self.assertEquals(sv._num_vars (), 1)

    #test if
    def test_if(self):
        prg1 = "if true then flag := 1"
        ast1 = ast.parse_string(prg1)
        print (ast1)
        sv = stats_visitor.StatsVisitor()
        sv.visit(ast1)
        self.assertEquals(sv.get_num_stmts(), 2)
        self.assertEquals(sv.get_num_vars(), 1)

    def test_if2(self):
        prg1 = "if false then flag := 1 else flag := 2"
        ast1 = ast.parse_string(prg1)
        print (ast1)
        sv = stats_visitor.StatsVisitor()
        sv.visit(ast1)
        self.assertEquals(sv.get_num_stmts(), 3)
        self.assertEquals(sv.get_num_vars(), 1)

    # test while
    def test_while(self):
        prg1 = "while true do flag := 1"
        ast1 = ast.parse_string(prg1)
        print (ast1)
        sv = stats_visitor.StatsVisitor()
        sv.visit(ast1)
        self.assertEquals(sv.get_num_stmts(), 2)
        self.assertEquals(sv.get_num_vars(), 1)

    # test havoc
    def test_havoc(self):
        prg1 = "havoc x"
        ast1 = ast.parse_string(prg1)
        print (ast1)
        sv = stats_visitor.StatsVisitor()
        sv.visit(ast1)
        self.assertEquals(sv.get_num_stmts(), 1)
        self.assertEquals(sv.get_num_vars(), 1)

    # test exp
    def test_exp(self):
        prg1 = "x := 1+3"
        ast1 = ast.parse_string(prg1)
        print (ast1)
        sv = stats_visitor.StatsVisitor()
        sv.visit(ast1)
        self.assertEquals(sv.get_num_stmts(), 1)
        self.assertEquals(sv.get_num_vars(), 1)

    # test assert
    def test_assert(self):
        prg1 = "assert 0 > 1"
        ast1 = ast.parse_string(prg1)
        print (ast1)
        sv = stats_visitor.StatsVisitor()
        sv.visit(ast1)
        self.assertEquals(sv.get_num_stmts(), 1)
        self.assertEquals(sv.get_num_vars(), 0)

    # test assume
    def test_assume(self):
        prg1 = "x := 1; assume x > 0"
        ast1 = ast.parse_string(prg1)
        print (ast1)
        sv = stats_visitor.StatsVisitor()
        sv.visit(ast1)
        self.assertEquals(sv.get_num_stmts(), 2)
        self.assertEquals(sv.get_num_vars(), 1)