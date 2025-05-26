from Token import Types
from ast_nodes import *

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, msg="Invalid syntax"):
        raise Exception(f"Parser error: {msg}")

    def advance(self):
        self.current_token = self.lexer.get_next_token()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.advance()
        else:
            self.error(f"Expected token {token_type} but got {self.current_token.type}")

    def parse(self):
        statements = []
        while self.current_token.type != Types.EOF:
            stmt = self.statement()
            if stmt:
                statements.append(stmt)
        return statements

    def statement(self):
        if self.current_token.type == Types.PRINT:
            self.eat(Types.PRINT)
            expr = self.expr()
            return Print(expr)

        elif self.current_token.type == Types.IDENTIFIER:
            var_token = self.current_token
            next_token = self.lexer.peek_next_token()
            if next_token.type == Types.ASSIGN:
                self.eat(Types.IDENTIFIER)
                self.eat(Types.ASSIGN)
                expr = self.expr()
                return Assign(var_token, expr)
            else:
                return self.expr()

        else:
            return self.expr()


    def expr(self):
        return self.logical_or()

    def logical_or(self):
        node = self.logical_and()
        while self.current_token.type == Types.OR:
            op = self.current_token
            self.advance()
            node = BinOp(left=node, op=op, right=self.logical_and())
        return node

    def logical_and(self):
        node = self.equality()
        while self.current_token.type == Types.AND:
            op = self.current_token
            self.advance()
            node = BinOp(left=node, op=op, right=self.equality())
        return node

    def equality(self):
        node = self.comparison()
        while self.current_token.type in (Types.EQ, Types.NOTEQ):
            op = self.current_token
            self.advance()
            node = BinOp(left=node, op=op, right=self.comparison())
        return node

    def comparison(self):
        node = self.term()
        while self.current_token.type in (Types.LTHAN, Types.GTHAN, Types.LTHANE, Types.GTHANE):
            op = self.current_token
            self.advance()
            node = BinOp(left=node, op=op, right=self.term())
        return node

    def term(self):
        node = self.factor()
        while self.current_token.type in (Types.PLUS, Types.MINUS):
            op = self.current_token
            self.advance()
            node = BinOp(left=node, op=op, right=self.factor())
        return node

    def factor(self):
        node = self.unary()
        while self.current_token.type in (Types.MULTIPLY, Types.DIVIDE):
            op = self.current_token
            self.advance()
            node = BinOp(left=node, op=op, right=self.unary())
        return node

    def unary(self):
        if self.current_token.type in (Types.NOT, Types.MINUS):
            op = self.current_token
            self.advance()
            node = UnaryOp(op=op, expr=self.unary())
            return node
        return self.primary()

    def primary(self):
        token = self.current_token

        if token.type in (Types.INTEGER, Types.FLOAT):
            self.advance()
            return Number(token.value)

        if token.type == Types.BOOLEAN:
            self.advance()
            return Boolean(token.value)

        if token.type == Types.STRING:
            self.advance()
            return String(token.value)

        if token.type == Types.IDENTIFIER:
            self.advance()
            return Var(token)

        if token.type == Types.LPAREN:
            self.advance()
            node = self.expr()
            self.eat(Types.RPAREN)
            return node

        self.error("Unexpected token in expression")
