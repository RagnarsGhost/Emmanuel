class AST:
    pass


class BinOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right



class UnaryOp:
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr


class Num:
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __repr__(self):
        return f"Num({self.value})"

class Boolean:
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __repr__(self):
        return f"Boolean({self.value})"