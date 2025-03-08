from Token import Types
from ast_nodes import BinOp, UnaryOp, Num, Boolean, String

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = None
        self.advance()

    def advance(self):
        self.current_token = self.lexer.get_next_token()

    def expr(self):
        # Simple implementation for an expression
        left = self.term()
        while self.current_token.type in (Types.PLUS, Types.MINUS):
            op = self.current_token
            self.advance()
            right = self.term()

            if isinstance(left, String) or isinstance(right, String):
                if op.type == Types.PLUS:
                    left = BinOp(left, op, right)
                else:
                    raise Exception("invalid operation on strings")
            else:
                left = BinOp(left, op, right)  # Create a BinOp node
        return left

    def term(self):
        # Parse multiplication and division
        left = self.factor()
        while self.current_token.type in (Types.MULTIPLY, Types.DIVIDE):
            op = self.current_token
            self.advance()
            right = self.factor()
            left = BinOp(left, op, right)  # Create a BinOp node
        return left

    def factor(self):
        # Parse numbers and parentheses
        token = self.current_token
        if token.type == Types.STRING:
            self.advance()
            return String(token)

        if token.type == Types.MINUS:
            self.advance()  # Skip the MINUS
            node = self.factor()  # Recursively parse the factor after unary minus
            return UnaryOp(op=token, expr=node)

        if token.type == Types.NOT:
            self.advance()
            node = self.factor()
            return UnaryOp(op=token, expr=node)

        if token.type == Types.BOOLEAN:
            self.advance()
            return Boolean(token)

        if token.type == Types.INTEGER or token.type == Types.FLOAT:
            self.advance()
            return Num(token)  # Return a Num node
        elif token.type == Types.LPAREN:
            self.advance()
            node = self.logical_or()
            if self.current_token.type != Types.RPAREN:
                raise Exception("Expected ')'")
            self.advance()
            return node
        else:
            raise Exception("Invalid syntax")

    def logical_or(self):
        node = self.logical_and()
        while self.current_token.type == Types.OR:
            op = self.current_token
            self.advance()
            right = self.logical_and()
            node = BinOp(left=node, op=op, right=right)
        return node

    def logical_and(self):
        node = self.equality()
        while self.current_token.type == Types.AND:
            op = self.current_token
            self.advance()
            right = self.equality()
            node = BinOp(left=node, op=op, right=right)
        return node

    def equality(self):
        node = self.comparison()
        while self.current_token.type in (Types.EQ, Types.NOTEQ):
            op = self.current_token
            self.advance()
            right = self.comparison()

            if isinstance(node, String) or isinstance(right, String):
               if op.type in (Types.EQ, Types.NOTEQ):
                   node = BinOp(left=node, op=op, right=right)
               else:
                   raise Exception("Invalid Comparison with String")
            else:
                 node = BinOp(left=node, op=op, right=right)
        return node

    def comparison(self):
        node = self.expr()
        while self.current_token.type in (Types.LTHAN, Types.GTHAN, Types.LTHANE, Types.GTHANE):
            op = self.current_token
            self.advance()
            right = self.expr()
            node = BinOp(left=node, op=op, right=right)
        return node


    def parse(self):
        return self.logical_or()