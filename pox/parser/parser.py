# coding: utf-8

from pox.parser.exprs import *
from pox.scanner import Token, TokenType

class Parser:
    current = 0

    def __init__(self, tokens: list[Token]):
        self.tokens = tokens

    def peek(self) -> Token:
        return self.tokens[self.current]

    def is_at_end(self) -> bool:
        return self.peek().type == TokenType.EOF

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1

        return self.previous()

    def check(self, t):
        if self.is_at_end():
            return False

        return self.peek().type == t

    def match(self, types: list[TokenType]) -> bool:
        for t in types:
            if self.check(t):
                self.advance()
                return True

        return False
