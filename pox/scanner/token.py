# coding: utf-8

from enum import Enum
from typing import Any

TokenType = Enum('TokenType', '''\
    LEFT_PAREN RIGHT_PAREN LEFT_BRACE RIGHT_BRACE
    COMMA DOT MINUS PLUS SEMICOLON SLASH STAR

    BANG BANG_EQUAL
    EQUAL EQUAL_EQUAL
    GREATER GREATER_EQUAL
    LESS LESS_EQUAL

    IDENTIFIER STRING NUMBER

    AND CLASS ELSE FALSE FUN FOR IF NIL OR
    PRINT RETURN SUPER THIS TRUE VAR WHILE

    EOF\
''')

class Token:
    def __init__(self, type: TokenType, lexeme: str, literal: Any, line: int):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self) -> str:
        return f'Token<{self.type.name}{": " + str(self.lexeme) if self.lexeme else ""}, {self.line}>'

    def __repr__(self) -> str:
        return self.__str__()
