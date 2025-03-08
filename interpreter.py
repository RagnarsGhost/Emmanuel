from Token import Types
from ast import BinOp, UnaryOp, Num, Boolean

class Interpreter:
    def __init__(self, parser):
        self.parser = parser

    def visit(self, node):
        """
        Dispatch method to visit a node.
        """
        method_name = 'visit_' + type(node).__name__  # 'visit_BinOp'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)


    def generic_visit(self, node):
        raise Exception(f"No visit_{type(node).__name__} method")

    def visit_BinOp(self, node):
        if node.op.type == Types.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == Types.MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == Types.MULTIPLY:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == Types.DIVIDE:
            return self.visit(node.left) / self.visit(node.right)
        elif node.op.type == Types.LTHAN:
            return self.visit(node.left) < self.visit(node.right)
        elif node.op.type == Types.GTHAN:
            return self.visit(node.left) > self.visit(node.right)
        elif node.op.type == Types.LTHANE:
            return self.visit(node.left) <= self.visit(node.right)
        elif node.op.type == Types.GTHANE:
            return self.visit(node.left) >= self.visit(node.right)
        elif node.op.type == Types.EQ:
            return self.visit(node.left) == self.visit(node.right)
        elif node.op.type == Types.NOTEQ:
            return self.visit(node.left) != self.visit(node.right)
        elif node.op.type == Types.AND:
            return self.visit(node.left) and self.visit(node.right)
        elif node.op.type == Types.OR:
            return self.visit(node.left) or self.visit(node.right)
        else:
            raise Exception(f"unknown binary operator")


    def visit_UnaryOp(self, node):
        if node.op.type == Types.PLUS:
            return +self.visit(node.expr)
        elif node.op.type == Types.MINUS:
            return -self.visit(node.expr)
        elif node.op.type == Types.NOT:
            return not self.visit(node.expr)
        else:
            raise Exception(f"unknown unary operator")

    def visit_Num(self, node):
        return node.value

    def visit_Boolean(self, node):
        return node.value

    def interpret(self):
        tree = self.parser.parse()
        #print("AST tree", tree)
        if tree is None:
            raise Exception("parser returned none")
        return self.visit(tree)