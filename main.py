#from IPython.utils.coloransi import value
from lexer import Lexer
from Token import Types
import sys


#from enum import Enum

def read_lexer_from_file(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        if not line:
            continue
        print(f"Expression: {line}")
        lexer = Lexer(line)
        while True:
            token = lexer.get_next_token()
            print(token)
            if token.type == Types.EOF:
                break
        print("-" * 30)


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
    def __init__(self, value):
        #self.token = token
        self.value = value

    def __repr__(self):
        return f"Num({self.value})"


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
        if token.type == Types.MINUS:
            self.advance()  # Skip the MINUS
            node = self.factor()  # Recursively parse the factor after unary minus
            return UnaryOp(op=token, expr=node)

        if token.type == Types.INTEGER or token.type == Types.FLOAT:
            self.advance()
            return Num(token.value)  # Return a Num node
        elif token.type == Types.LPAREN:
            self.advance()
            node = self.expr()  # Recursively parse the expression inside parentheses
            if self.current_token.type != Types.RPAREN:
                raise Exception("Expected ')'")
            self.advance()
            return node
        else:
            raise Exception("Invalid syntax")

    def parse(self):
        return self.expr()  # Start parsing from the 'expr' method



# -----------------------
# INTERPRETER (AST EVALUATOR)
# -----------------------

class Interpreter:
    def __init__(self, parser):
        self.parser = parser

    def visit(self, node):
        """
        Dispatch method to visit a node.
        """
        method_name = 'visit_' + type(node).__name__  # 'visit_BinOp'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)  # This should pass the node correctly



    def generic_visit(self, node):
        raise Exception(f"No visit_{type(node).__name__} method")

    def visit_BinOp(self, node):
    # Ensure that 'node' has left, op, and right attributes
     if node.op.type == Types.PLUS:
        return self.visit(node.left) + self.visit(node.right)
     elif node.op.type == Types.MINUS:
        return self.visit(node.left) - self.visit(node.right)
     elif node.op.type == Types.MULTIPLY:
        return self.visit(node.left) * self.visit(node.right)
     elif node.op.type == Types.DIVIDE:
        return self.visit(node.left) / self.visit(node.right)

    def visit_UnaryOp(self, node):
        if node.op.type == Types.PLUS:
            return +self.visit(node.expr)
        elif node.op.type == Types.MINUS:
            return -self.visit(node.expr)

    def visit_Num(self, node):
        return node.value

    def interpret(self):
        tree = self.parser.parse()
        #print("AST tree", tree)
        if tree is None:
            raise Exception("parser returned none")
        return self.visit(tree)


"""
if read_lexer_from_file == "__main__":
    if len(sys.argv) > 1:
        source_file = sys.argv[1]
else:
    source_file = "C:\\Users\\ldi\\Language Design\\test.src"  # Default file path
    read_lexer_from_file("C:\\Users\\ldi\\Language Design\\test.src")
"""
if __name__ == "__main__":
    # Use the command-line argument if provided, otherwise use a default file path.
    if len(sys.argv) > 1:
        source_file = sys.argv[1]
    else:
        source_file = "C:\\Users\\ldi\\Language Design\\test.src"  # Default file path

    # Optionally, if you want to see the token stream for debugging, uncomment this line:
    # read_lexer_from_file(source_file)

    # Now process the file to evaluate the arithmetic expressions.
    try:
        with open(source_file, "r") as file:
            lines = file.readlines()
    except IOError:
        print(f"Error: Could not open file {source_file}")
        sys.exit(1)

    for line in lines:
        line = line.strip()
        if not line:
            continue  # Skip blank lines
        print(f"Expression: {line}")
        try:
            # Create a new lexer, parser, and interpreter for each expression
            lexer = Lexer(line)
            parser = Parser(lexer)
            interpreter = Interpreter(parser)
            result = interpreter.interpret()
            print(f"{line} = {result}")
        except Exception as e:
            print(f"Error processing expression '{line}': {e}")
        print("-" * 30)
