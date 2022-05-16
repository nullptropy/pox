# coding: utf-8

from pox.parser.exprs import *
from pox.scanner import TokenType
from pox.utils import build_parse_error

class ParserError(Exception):
    pass

class Parser:
    current = 0

    def __init__(self, tokens):
        self.tokens = tokens

    def peek(self):
        return self.tokens[self.current]

    def is_at_end(self):
        return self.peek().type == TokenType.EOF

    def previous(self):
        return self.tokens[self.current - 1]

    def advance(self):
        if not self.is_at_end():
            self.current += 1

        return self.previous()

    def check(self, t):
        if self.is_at_end():
            return False

        return self.peek().type == t

    def match(self, *types):
        for t in types:
            if self.check(t):
                self.advance(); return True

        return False

    def error(self, message):
        return ParserError(build_parse_error(self, message))
