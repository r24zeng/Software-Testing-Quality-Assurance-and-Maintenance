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

import sys

class M (object):
    def m (self, arg, i):
        q = 1
        o = None

        nothing = Impossible ()
        if i == 0:
            q = 4
        q = q + 1
        n = len (arg)
        if n == 0:
            q = q / 2
        elif n == 1:
            o = A ()
            B ()
            q = 25
        elif n == 2:
            o = A ()
            q = q * 100
            o = B ()
        else:
            o = B ()
        if n > 0:
            o.m ()
        else:
            print 'zero'
        nothing.happened()

class A (object):
    def m (self):
        print 'a'
class B (A):
    def m (self):
        print 'b'
class Impossible (object):
    def happened(self):
        pass

def main (argv):
    obj = M ()
    if len (argv) > 1:
        obj.m (argv [1], len (argv))
    
    
