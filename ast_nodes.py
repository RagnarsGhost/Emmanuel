class AST:
    pass

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class UnaryOp(AST):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

class Number(AST):
    def __init__(self, value):
        self.value = value

class Boolean(AST):
    def __init__(self, value):
        self.value = value

class String(AST):
    def __init__(self, value):
        self.value = value

class Var(AST):
    def __init__(self, name_token):
        self.name = name_token.value

class Assign(AST):
    def __init__(self, name_token, expr):
        self.name = name_token.value
        self.expr = expr

class Print(AST):
    def __init__(self, expr):
        self.expr = expr
