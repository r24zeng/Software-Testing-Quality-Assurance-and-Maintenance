import unittest
import wlang.ast as ast
import wlang.undef_visitor as undef_visitor

class TestStatsVisitor (unittest.TestCase):
    def test_one (self):
        prg1 = "x := 10; y := x + z"
        ast1 = ast.parse_string (prg1)
        print (ast1)
        uv = undef_visitor.UndefVisitor ()
        uv.check (ast1)
        # UNCOMMENT to run the test
        self.assertEquals (set ([ast.IntVar('z')]), uv.get_undefs ())

    # test havoc
    def test_havoc(self):
        prg1 = "havoc x, y"
        ast1 = ast.parse_string (prg1)
        print (ast1)
        uv = undef_visitor.UndefVisitor ()
        uv.check (ast1)
        self.assertTrue(len(uv.get_undefs ()) == 0)

    # test if
    def test_if(self):
        prg1 = "if true then x := x+1; if false then skip else {y := 1; z := z+1}"
        ast1 = ast.parse_string(prg1)
        print (ast1)
        uv = undef_visitor.UndefVisitor()
        uv.check(ast1)
        self.assertEquals(set([ast.IntVar('x'),ast.IntVar('z')]), uv.get_undefs())

    # test while
    def test_while(self):
        prg1 = "while true do a := a+b"
        ast1 = ast.parse_string(prg1)
        print (ast1)
        uv = undef_visitor.UndefVisitor()
        uv.check(ast1)
        self.assertEquals(set([ast.IntVar('a'), ast.IntVar('b')]), uv.get_undefs())

    # test assert
    def test_assert(self):
        prg1 = "assert a > 0"
        ast1 = ast.parse_string(prg1)
        print (ast1)
        uv = undef_visitor.UndefVisitor()
        uv.check(ast1)
        self.assertEquals(set([ast.IntVar('a')]), uv.get_undefs())

    # test assume
    def test_assume(self):
        prg1 = " x := 10; assume x > 0"
        ast1 = ast.parse_string(prg1)
        print (ast1)
        uv = undef_visitor.UndefVisitor()
        uv.check(ast1)
        self.assertTrue(len(uv.get_undefs()) == 0)
