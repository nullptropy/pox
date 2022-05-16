# coding: utf-8

from pox.utils import build_syntax_error, decode_escapes
from pox.scanner.token import Token, TokenType, RESERVED_KEYWORDS

class ScannerError(Exception):
    pass

class Scanner:
    line = 1
    start = 0
    current = 0

    def __init__(self, source: str):
        self.source = source

    def error(self, message):
        raise ScannerError(build_syntax_error(self, message))

    def scan_tokens(self):
        tokens = []

        while not self.is_at_end():
            try:
               tokens.append(self.scan_token())
            except ScannerError as err:
                print(err)

        return tokens + [Token(TokenType.EOF, "", None, self.line)]

    def scan_token(self):
        self.start = self.current

        match c := self.advance():
            case '(': return self.make_token(TokenType.LEFT_PAREN)
            case ')': return self.make_token(TokenType.RIGHT_PAREN)
            case '{': return self.make_token(TokenType.LEFT_BRACE)
            case '}': return self.make_token(TokenType.RIGHT_BRACE)
            case ',': return self.make_token(TokenType.COMMA)
            case '.': return self.make_token(TokenType.DOT)
            case '+': return self.make_token(TokenType.PLUS)
            case '-': return self.make_token(TokenType.MINUS)
            case '*': return self.make_token(TokenType.STAR)
            case ';': return self.make_token(TokenType.SEMICOLON)

            case '=':
                return self.make_token(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
            case '!':
                return self.make_token(TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG)
            case '<':
                return self.make_token(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS)
            case '>':
                return self.make_token(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER)

            case ' ' | '\r' | '\t': pass
            case '\n': self.line += 1
            case '/':
                if not self.match('/', '*'):
                    return self.make_token(TokenType.SLASH)

                self.scan_comment(self.source[self.current - 1])

            case '\'' | '"': return self.scan_string(c)
            case c if c.isdigit(): return self.scan_number()
            case c if c.isalpha(): return self.scan_identifier()

            case _:
                self.error(f'unexpected character: {repr(c)}')

    def is_at_end(self):
        return self.current >= len(self.source)

    def advance(self):
        try:
            return self.source[self.current]
        finally:
            self.current += 1

    def peek(self, n=1):
        if self.is_at_end():
            return '\0'

        return self.source[self.current + n - 1]

    def match(self, *expected):
        if self.is_at_end() or self.source[self.current] not in expected:
            return False

        self.current += 1
        return True

    def make_token(self, type, literal=None):
        return Token(type, self.source[self.start:self.current], literal, self.line)

    def scan_number(self):
        while self.peek().isdigit():
            self.advance()

        if self.peek() == '.' and self.peek(2).isdigit():
            self.advance()

            while self.peek().isdigit():
                self.advance()

        return self.make_token(TokenType.NUMBER, float(self.source[self.start:self.current]))

    def scan_identifier(self):
        while self.peek().isalnum() or self.peek() == '_':
            self.advance()

        return self.make_token(
            RESERVED_KEYWORDS.get(self.source[self.start:self.current], TokenType.IDENTIFIER))

    def scan_string(self, quote):
        while self.peek() not in ['\0', quote]:
            if self.peek() == '\n':
                self.line += 1

            self.advance()

        if self.is_at_end():
            self.error('unterminated string')

        self.advance()

        return self.make_token(
            TokenType.STRING,
            decode_escapes(self.source[self.start + 1:self.current - 1]))

    def scan_comment(self, comment):
        match comment:
            case '/':
                while self.peek() not in ['\0', '\n']:
                    self.advance()

            case '*':
                while not self.is_at_end() and (self.peek() != '*' or self.peek(2) != '/'):
                    if self.peek() == '\n':
                        self.line += 1

                    self.advance()

                if self.is_at_end():
                    self.error('unterminated multi-line comment')

                self.advance()
                self.advance()
