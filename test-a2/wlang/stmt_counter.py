from __future__ import print_function

import wlang.ast 

class StmtCounterStateless (wlang.ast.AstVisitor):
    def __init__ (self):
        super (StmtCounterStateless, self).__init__ ()

    def visit_StmtList (self, node, *args, **kwargs):
        if node.stmts is None:
            return 0
        res = 0
        for s in node.stmts:
            res = res + self.visit (s)
        return res

    def visit_IfStmt (self, node, *args, **kwargs):
        res = 1 + self.visit (node.then_stmt)
        if node.has_else ():
            res = res + self.visit (node.else_stmt)
        return res

    def visit_WhileStmt (self, node, *args, **kwargs):
        return 1 + self.visit (node.body)
    
    def visit_Stmt (self, node, *args, **kwargs):
        return 1


class StmtCounterStatefull (wlang.ast.AstVisitor):
    def __init__ (self):
        super (StmtCounterStatefull, self).__init__ ()
        self._count = 0

    def get_num_stmts (self):
        return self._count

    def count (self, node, *args, **kwargs):
        self._count = 0
        self.visit (node, *args, **kwargs)

    def visit_StmtList (self, node, *args, **kwargs):
        if node.stmts is None:
            return
        for s in node.stmts:
            self.visit (s)
            
    def visit_Stmt (self, node, *args, **kwargs):
        self._count = self._count + 1
    def visit_IfStmt (self, node, *args, **kwargs):
        self.visit_Stmt (node)
        self.visit (node.then_stmt)
        if node.has_else ():
            self.visit (node.else_stmt)

    def visit_WhileStmt (self, node, *args, **kwargs):
        self.visit_Stmt (node)
        self.visit (node.body)

if __name__ == '__main__':
    prg1 = 'x := 10; if y > 10 then x := x + 1 else x := x - 1 ; print_state'
    ast1 = wlang.ast.parse_string (prg1)
    sc1 = StmtCounterStateless ()
    print ('Input program is')
    print (ast1)
    print ('Number of statements by sc1 is:', sc1.visit (ast1))
    sc2 = StmtCounterStatefull ()
    sc2.count (ast1)
    print ('Number of statements by sc2 is:', sc2.get_num_stmts ())
