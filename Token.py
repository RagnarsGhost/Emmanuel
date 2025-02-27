from enum import Enum

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
    NOTEQ = "NOTEQ"
    BOOLEAN ="BOOLEAN"
    EOF = "EOF"

class Token:
    def __init__(self, type, value, supertype=None, precedence=None):
        self.type = type
        self.value = value
        self.supertype = supertype
        self.precedence = precedence

    def __repr__(self):
        return f"Token({self.type}, {self.value}, {self.supertype}, {self.precedence})"
