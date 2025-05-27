from enum import Enum
from typing import Dict, Any, Tuple

class Types(Enum):
    NUMBER = "NUMBER"
    FLOAT = "FLOAT"
    INTEGER = "INTEGER"
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LTHAN = "LTHAN"
    GTHAN = "GTHAN"
    LTHANE = "LTHANE"
    GTHANE = "GTHANE"
    NOT = "NOT"
    AND = "AND"
    OR = "OR"
    EQ = "EQ"
    ASSIGN = "ASSIGN"
    NOTEQ = "NOTEQ"
    BOOLEAN ="BOOLEAN"
    STRING = "STRING"
    DEL = "DEL"
    EOF = "EOF"

    #keywords
    TRUE = "TRUE"
    FALSE = "FALSE"
    ELSE ="else"
    WHILE = "while"
    IF = "if"
    CLASS = "class"
    THIS = "this"
    NULL = "null"
    FUNCTION = "function"
    RETURN = "return"
    FOR = "for"
    SUPER ="super"
    CONST = "const"
    LET = "let"
    VAR = "var"
    PRINT = "print"
    IDENT = "IDENT"

    # String starters
    SINGLE_QUOTE = "'"
    DOUBLE_QUOTE = '"'

    # New line
    NEW_LINE = '\n'

    # Space
    TAB = '\t'
    SPACE = ' '

    # String terminator
    NULL_CHARACTER = '\0'

    # Backslash
    BACKSLASH = '\\'

    #Escaped quotes
    ESCAPED_QUOTES = '\"', '\''

    # End-user identifiers
    IDENTIFIER = 'IDENTIFIER'

_keywords: Tuple[str, ...] = (
    "TRUE", "FALSE", "null", "AND", "OR", "if", "else", "function", "return",
    "for", "class", "super", "this", "const", "let", "while", "var", "print"
)

KEYWORDS: Dict[str, Types] = {key: Types(key) for key in _keywords}

SINGLE_CHARS: Tuple[str, ...] = (
    '(', ')', '{', '}', ',', '.', '-', '+', ';', '*',
)

ONE_OR_MORE_CHARS: Tuple[str, ...] = ('!', '!=', '==', '>', '>=', '<', '<=')

WHITESPACE: Tuple[str, ...] = (' ', '\r', '\t')

STRING_STARTERS: Tuple[str, ...] = ('"', "'")

class Token:
    def __init__(self, type, value, supertype=None, precedence=None):
        self.type = type
        self.value = value
        self.supertype = supertype
        self.precedence = precedence

    def __repr__(self):
        return f"Token({self.type}, {self.value}, {self.supertype}, {self.precedence})"
