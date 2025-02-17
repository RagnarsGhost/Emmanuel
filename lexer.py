from Token import Token
from Token import Types
class Lexer:
    def __init__(self, text):
        self.text = text
        self.position = 0
        self.current_char = self.text[self.position] if self.text else None

    def error(self):
        raise Exception("Invalid character encountered")

    def advance(self):
        """Move to the next character in the input text."""
        self.position += 1
        if self.position >= len(self.text):
            self.current_char = None  # End of input
        else:
            self.current_char = self.text[self.position]

    def skip_whitespace(self):
        """Skip any whitespace characters."""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def number(self):
        """
        Handle numbers (integer and float). A valid number can include
        digits and an optional decimal point.
        """
        result = ''
        dot_count = 0
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                dot_count += 1
                if dot_count > 1:
                    break  # More than one decimal point is invalid
            result += self.current_char
            self.advance()
        # Convert to int if no decimal point, else float.
        if dot_count == 0:
            return Token(Types.INTEGER, int(result))
        elif dot_count == 1:
            return Token(Types.FLOAT, float(result))
        #return Token(Types.NUMBER, float(result) if dot_count == 1 else int(result))

    def get_next_token(self):
        """Lexical analyzer that breaks the input into tokens."""
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit() or self.current_char == '.':
                return self.number()

            if self.current_char == '+':
                self.advance()
                return Token(Types.PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(Types.MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(Types.MULTIPLY, '*')

            if self.current_char == '/':
                self.advance()
                return Token(Types.DIVIDE, '/')

            if self.current_char == '(':
                self.advance()
                return Token(Types.LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(Types.RPAREN, ')')

            self.error()

        return Token(Types.EOF, None)
