# coding: utf-8

from .token import Token, TokenType
from result import Ok, Err, Result

class Scanner:
    line = 1
    start = 0
    current = 0

    def __init__(self, source: str):
        self.source = source
        self.eof_token = False

    def __iter__(self):
        return self

    def __next__(self) -> Result[Token, str] | None:
        self.start = self.current

        if self.eof_token:
            raise StopIteration

        if self.is_at_end():
            self.eof_token = True
            return Ok(Token(TokenType.EOF, "", None, self.line))

        return self.scan_token()

    def scan_token(self) -> Result[Token, str] | None:
        match c := self.advance():
            case '(': return Ok(self.make_token(TokenType.LEFT_PAREN))
            case ')': return Ok(self.make_token(TokenType.RIGHT_PAREN))
            case '{': return Ok(self.make_token(TokenType.LEFT_BRACE))
            case '}': return Ok(self.make_token(TokenType.RIGHT_BRACE))
            case ',': return Ok(self.make_token(TokenType.COMMA))
            case '.': return Ok(self.make_token(TokenType.DOT))
            case '+': return Ok(self.make_token(TokenType.PLUS))
            case '-': return Ok(self.make_token(TokenType.MINUS))
            case '*': return Ok(self.make_token(TokenType.STAR))

            case '=':
                return Ok(self.make_token(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL))
            case '!':
                return Ok(self.make_token(TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG))
            case '<':
                return Ok(self.make_token(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS))
            case '>':
                return Ok(self.make_token(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER))

            case ' ' | '\r' | '\t': pass
            case '\n': self.line += 1

            case '/':
                if not self.match('/'):
                    return Ok(self.make_token(TokenType.SLASH))

                while (self.peek() != '\n' and not self.is_at_end()):
                    self.advance()

            case _:
                return Err(f'{self.line} | unexpected character: {repr(c)}')

    def is_at_end(self):
        return self.current >= len(self.source)

    def advance(self) -> str:
        try:
            return self.source[self.current]
        finally:
            self.current += 1

    def peek(self) -> str:
        if self.is_at_end():
            return '\0'

        return self.source[self.current]

    def match(self, expected: str) -> bool:
        if self.is_at_end():
            return False

        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def make_token(self, type, literal=None) -> Token:
        return Token(type, self.source[self.start:self.current], literal, self.line)
