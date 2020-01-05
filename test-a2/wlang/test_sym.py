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

def print_result(states):
    out = []
    result = []
    if states is None:
        print '[symexec]: no output states'
    else:
        count = 0
        for state in states:
            count = count + 1
            print '[symexec]: symbolic state reached'
            out.append(state)
            result.append(state.pick_concerete())
            #res = state.pick_concerete()
            #result.append(res.env.values())
        print '[symexec]: found', count, 'symbolic states'
    for result in result:
        print(result)
    return out

class TestSym (unittest.TestCase):
    def test_one (self):
        prg1 = "havoc x; assume x > 10; assert x > 15"
        ast1 = ast.parse_string (prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        out = [s for s in sym.run (ast1, st)]
        print out
        list_result=[]
        if out is None:
            print ('[symexec]: no output states')
        else:
            count = 0
            for state in out:
                count = count + 1
                print ('[symexec]: symbolic state reached')
                print (state)
                result = state.pick_concerete()
                list_result.append(result)
            print ('[symexec]: found', count, 'symbolic states')
        for result in list_result:
           print(result)
        self.assertEquals (len(out), 1)

    def test_two(self):
        # test if-then-else , assignment and <=, >=, <, > in if and -, +, %
        prg1 = "x := 8; if x <= 10 then x := x-1; if x >= 10 then skip else x := x*2; if x < 0 then x := 2; if x > 0 then x := x%10"
        ast1 = ast.parse_string (prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        states = sym.run (ast1, st)
        out = print_result(states)
        self.assertEquals (len(out), 1)

    def test_three(self):
        # test if and skip and violated assert
        prg1 = "havoc x; y := 0; if true then skip else y := 1; if false then skip; assert y = 1; if x=y then x := 1; " \
               "if x > 1 then y := 1 else x := 0 "
        ast1 = ast.parse_string (prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        states = sym.run (ast1, st)
        out = print_result(states)
        self.assertEquals (len(out), 0)

    def test_four(self):
        # test *, %, /, not
        prg1 = "havoc x, y, z, q; q := 1; x := x/3; y := y*2; if not x < y then z := z/10; assert q > 0"
        ast1 = ast.parse_string (prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        states = sym.run (ast1, st)
        out = print_result(states)
        self.assertEquals (len(out), 1)

    def test_five(self):
        # test and, or, while-do, stmlist
        prg1 = "x := 2; {y := 10; z := 15}; while x > 0 and y < 11 or z < 1 do {x := x/3; print_state}"
        ast1 = ast.parse_string (prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        states = sym.run (ast1, st)
        out = print_result(states)
        self.assertEquals (len(out), 1)

    def test_six(self):
        # test arithmetic in while
        prg1 = "a := 5; while a <= 10 do a := a+1; b := 5; while b < 10 do b := b+1; c := 5; while c >= 1 do c := c-1; " \
               "d := 5; while d > 1 do d := d-1; e := 5; while e = 5 do e := 1 "
        ast1 = ast.parse_string (prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        states = sym.run (ast1, st)
        out = print_result(states)
        self.assertEquals (len(out), 1)

    def test_six2(self):
        # test arithmetic in while
        prg1 = "havoc a, b, c, d, e, f; while a <= 5 do {f := 1}; while b < 5 do {f :=1}; while c >= 5 do {f := 2}; " \
               "while d > 5 do {f := 3}; while e = 5 do {f:= 4}"
        ast1 = ast.parse_string (prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        states = sym.run (ast1, st)
        out = print_result(states)
        self.assertEquals (len(out), 1)

    def test_six3(self):
        # test arithmetic in while
        prg1 = "{a := 1; f := 5}; while f <= a do {f := 1}; while f < a do {f := 2}; { b := 5; f := 1};" \
               "while f >= b do {f := 3}; while f > b do {f :=4}; while f = a do {f := 5}"
        ast1 = ast.parse_string (prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        states = sym.run (ast1, st)
        out = print_result(states)
        self.assertEquals (len(out), 1)

    def test_seven(self):
        # test arithmetic in if
        prg1 = "{ a:= 5; b := 5; c := 5; d := 5; e := 5}; while a = 5 do a := a -1; if a <= 10 then a := a+1; " \
               "if b < 10 then b := b+1; if c >= 1 then c := c-1; if d > 1 then d := d-1; if a = 5 then e := 1"
        ast1 = ast.parse_string (prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        states = sym.run (ast1, st)
        out = print_result(states)
        self.assertEquals(len(out), 1)

    def test_seven2(self):
        # test arithmetic in if
        prg1 = "havoc a, b, c, d, e; if a <= 10 then a := a+1; if b < 10 then b := b+1; if c >= 1 then c := c-1; " \
               "if d > 1 then d := d-1; if e = 5 then e := 1"
        ast1 = ast.parse_string (prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        states = sym.run (ast1, st)
        out = print_result(states)
        self.assertEquals(len(out), 32)

    def test_seven3(self):
        # test arithmetic in while
        prg1 = "{a := 1; f := 5}; if f <= a then f := 1; if f < a then f := 2; { b := 5; f := 1}; if f >= b then f := 3; " \
               "if f > b then f :=4; if f = b then f := 5"
        ast1 = ast.parse_string (prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        states = sym.run (ast1, st)
        out = print_result(states)
        self.assertEquals (len(out), 1)

    def test_seven4(self):
        # test arithmetic in while
        prg1 = "havoc a; if 1 <= a then f := 1; if 1 < a then f := 2; if 5 >= a then f := 3; " \
               "if 5 > a then f :=4; if 5 = a then f := 5"
        ast1 = ast.parse_string (prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        states = sym.run (ast1, st)
        out = print_result(states)
        self.assertEquals (len(out), 5)

    def test_eight(self):
        # test arithmetic in assert
        prg1 = "a := 5; assert a <= 10; assert a < 5; assert a = 5; assert a >= 5; assert a >5"
        ast1 = ast.parse_string (prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        states = sym.run (ast1, st)
        out = print_result(states)
        self.assertEquals(len(out), 0)

    def test_eight2(self):
        # test arithmetic in assert
        prg1 = "havoc a; assert a <= 10; assert a < 5; assert a = 5; assert a >= 5; assert a >5"
        ast1 = ast.parse_string (prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        states = sym.run (ast1, st)
        out = print_result(states)
        self.assertEquals(len(out), 0)

    def test_nine(self):
        # test arithmetic in assume
        prg1 = "havoc a; assume a <= 10; assume a < 5; assume a = 5; assume a >= 5; assume a >5"
        ast1 = ast.parse_string (prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        states = sym.run (ast1, st)
        out = print_result(states)
        self.assertEquals(len(out), 0)

    def test_me(self):
        # write a program on which symbolic execution engine diverges
        # takes long time to run < 2s 263ms >
        prg1 = "havoc x; if x < -100 then {f := 1; x := x/100}; if x < -10 then {f := 2; x := x/10}; if x < 0 then {f := 3;" \
               " x := x + 10}; if x > 0 then {f := 4; x := x*5}; if x >= 10 then {f := 5; x := x-20}; if x = 100 then {f := 6; x := 100} "
        ast1 = ast.parse_string (prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        states = sym.run (ast1, st)
        out = print_result(states)


