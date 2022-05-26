# coding: utf-8

from pox.scanner import TokenType
from pox.utils import build_parse_error

from pox.parser.exprs import *
from pox.parser.stmts import *

SYNC_TOKENS = [
    TokenType.IF, TokenType.FOR, TokenType.VAR, TokenType.FUN,
    TokenType.PRINT, TokenType.WHILE, TokenType.CLASS, TokenType.RETURN]

class ParseError(Exception):
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
        return ParseError(build_parse_error(self, message))

    def consume(self, t, message):
        if self.check(t):
            return self.advance()

        raise self.error(message)

    def synchronize(self):
        self.advance()

        while not self.is_at_end():
            if self.previous().type == TokenType.SEMICOLON or \
                    self.peek().type in SYNC_TOKENS:
                return

            self.advance()

    def parse(self):
        statements = []

        while not self.is_at_end():
            statements.append(self.statement())

        return statements

    def statement(self):
        if self.match(TokenType.PRINT):
            return self.print_statement()

        return self.expression_statement()

    def print_statement(self):
        value = self.expression()
        self.consume(TokenType.SEMICOLON, 'expect \';\' after value')
        return Print(value)

    def expression_statement(self):
        value = self.expression()
        self.consume(TokenType.SEMICOLON, 'expect \';\' after expression')
        return Expression(value)

    def expression(self):
        return self.equality()

    def equality(self):
        expr = self.comparison()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            expr = Binary(expr, self.previous(), self.comparison())

        return expr

    def comparison(self):
        expr = self.term()

        while self.match(
                TokenType.GREATER, TokenType.GREATER_EQUAL,
                TokenType.LESS, TokenType.LESS_EQUAL):
            expr = Binary(expr, self.previous(), self.term())

        return expr

    def term(self):
        expr = self.factor()

        while self.match(TokenType.MINUS, TokenType.PLUS):
            expr = Binary(expr, self.previous(), self.factor())

        return expr

    def factor(self):
        expr = self.unary()

        while self.match(TokenType.SLASH, TokenType.STAR):
            expr = Binary(expr, self.previous(), self.factor())

        return expr

    def unary(self):
        if self.match(TokenType.BANG, TokenType.MINUS):
            return Unary(self.previous(), self.unary())

        return self.primary()

    def primary(self):
        if self.match(TokenType.NIL): return Literal(None)
        if self.match(TokenType.TRUE): return Literal(True)
        if self.match(TokenType.FALSE): return Literal(False)

        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)

        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, 'expected \')\' after expression')
            return Grouping(expr)
