# coding: utf-8

from enum import Enum

TokenType = Enum('TokenType', '''
    LEFT_PAREN RIGHT_PAREN LEFT_BRACE RIGHT_BRACE
    COMMA DOT MINUS PLUS SEMICOLON SLASH STAR

    BANG BANG_EQUAL
    EQUAL EQUAL_EQUAL
    GREATER GREATER_EQUAL
    LESS LESS_EQUAL

    IDENTIFIER STRING NUMBER

    AND CLASS ELSE FALSE FN FOR IF NIL OR
    RETURN SUPER THIS TRUE LET WHILE

    EOF
''')

# this depends on all of the keywords being back to back
# and taking values in the range `[23, 39)`
RESERVED_KEYWORDS = {
    TokenType(n).name.lower(): TokenType(n) for n in range(23, 38)}

class Token:
    def __init__(self, type, lexeme, literal, line):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        return f'Token<{self.type.name}{": " + str(self.lexeme) if self.lexeme else ""}, {self.line}>'

    def __repr__(self):
        return self.__str__()
