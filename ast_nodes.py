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

class Del(AST):
    def __init__(self, name_token):
        self.name = name_token.value

class If(AST):
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

class While(AST):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class Input(AST):
    def __init__(self, prompt_expr):
        self.prompt_expr = prompt_expr

