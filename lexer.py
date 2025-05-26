from astropy.io.votable.validator.result import Result

from Token import Token
from Token import Types, _keywords


class Lexer:
    def __init__(self, text):
        self.text = text
        self.position = 0
        self.current_char = self.text[self.position] if self.text else None
        self._buffered_token = None

    def error(self):
        raise Exception("Invalid character encountered")

    def advance(self):
        """Move to the next character in the input text."""
        self.position += 1
        if self.position >= len(self.text):
            self.current_char = None  # End of input
        else:
            self.current_char = self.text[self.position]

    def peek(self):
        """Look ahead to the next character without consuming it."""
        peek_pos = self.position + 1
        if peek_pos >= len(self.text):
            return None
        return self.text[peek_pos]

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
        if dot_count == 0:
            return Token(Types.INTEGER, int(result))
        elif dot_count == 1:
            return Token(Types.FLOAT, float(result))

    def _identifier(self) -> str:
        """Collect a sequence of alphabetic characters into an identifier."""
        result = ''
        while self.current_char is not None and (self.current_char.isalpha() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        return result


    def get_string(self):
        qoute_type = self.current_char
        self.advance()
        result = ""
        while self.current_char is not None and self.current_char != qoute_type:
            if self.current_char == '\\':
                self.advance()
                if self.current_char == 'n':
                    result += '\n'
                elif self.current_char == 't':
                    result += '\t'
                elif self.current_char == '"':
                    result += '"'
                elif self.current_char == 'r':
                    result += '\r'
                elif self.current_char == '\\':
                    result += '\\'
                elif self.current_char == '0':
                    result += '\0'
                elif self.current_char == '\"':
                    result += '\"'
                elif self.current_char == '\'':
                    result += '\''
                elif self.current_char == 'x':
                    hex_digits = self.text[self.position+1:self.position+3]
                    if len(hex_digits) == 2 and all(c in "0123456789abcdefABCDEF" for c in hex_digits):
                        result += chr(int(hex_digits, 16))
                    self.advance()
                    self.advance()
                elif self.current_char == 'u':
                    uni_digits = self.text[self.position+1:self.position+5]
                    if len(uni_digits) == 4 and all(c in "0123456789abcdefABCDEF" for c in uni_digits):
                        result += chr(int(uni_digits, 16))
                    self.advance()
                    self.advance()
                    self.advance()
                    self.advance()
                else:
                    raise Exception("invalid escape sequence")
            else:
                result += self.current_char
            self.advance()
        if self.current_char != qoute_type:
            raise Exception("Unterminated string literal")
        self.advance()
        return Token(Types.STRING, result)


    def get_next_token(self):
        """Lexical analyzer that breaks the input into tokens."""
        if self._buffered_token:
            token = self._buffered_token
            self._buffered_token = None
            return token
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit() or self.current_char == '.':
                return self.number()

            if self.current_char in ('"', "'"):
                return self.get_string()


            if self.current_char.isalpha():
                id_str = self._identifier()

                if id_str == "print":
                    return Token(Types.PRINT, "print")

                if id_str == "true":
                    return Token(Types.BOOLEAN, True)
                elif id_str  == "false":
                    return Token(Types.BOOLEAN, False)
                elif id_str == "and":
                    return Token(Types.AND, "and")
                elif id_str  == "or":
                    return Token(Types.OR, "or")
                else:
                    return Token(Types.IDENTIFIER, id_str)

    # Handle multi-character operators
            if self.current_char == '<':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    return Token(Types.LTHANE, "<=")
                else:
                    self.advance()
                    return Token(Types.LTHAN, "<")

            if self.current_char == '>':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    return Token(Types.GTHANE, ">=")
                else:
                    self.advance()
                    return Token(Types.GTHAN, ">")

            if self.current_char == '=':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    return Token(Types.EQ, "==")
                else:
                    self.advance()
                    return Token(Types.ASSIGN, "=")

            if self.current_char == '!':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    return Token(Types.NOTEQ, "!=")
                else:
                    self.advance()
                    return Token(Types.NOT, "!")

            # Single-character tokens
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

    def peek_token(self):
        if not self._buffered_token:
            saved_position = self.position
            saved_char = self.current_char
            self._buffered_token = self.get_next_token()
            self.position = saved_position
            self.current_char = self.text[self.position] if self.position < len(self.text) else None
        return self._buffered_token

    def peek_next_token(self):
            saved_position = self.position
            saved_char = self.current_char

            # Read one token
            token = self.get_next_token()

            # Restore position and character
            self.position = saved_position
            self.current_char = self.text[self.position] if self.position < len(self.text) else None

            return token

