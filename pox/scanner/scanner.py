# coding: utf-8

from result import Ok, Err, Result

from pox.utils import build_syntax_error, decode_escapes
from pox.scanner.token import Token, TokenType, RESERVED_KEYWORDS

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
            case ';': return Ok(self.make_token(TokenType.SEMICOLON))

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
                if not self.match('/', '*'):
                    return Ok(self.make_token(TokenType.SLASH))

                match self.scan_comment(self.source[self.current - 1]):
                    case Err(error):
                        return Err(error)

            case '\'' | '"': return self.scan_string(c)
            case c if c.isdigit(): return self.scan_number()
            case c if c.isalpha(): return self.scan_identifier()

            case _:
                return Err(build_syntax_error(self, f'unexpected character: {repr(c)}'))

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def advance(self) -> str:
        try:
            return self.source[self.current]
        finally:
            self.current += 1

    def peek(self, n=1) -> str:
        if self.is_at_end():
            return '\0'

        return self.source[self.current + n - 1]

    def match(self, *expected) -> bool:
        if self.is_at_end() or self.source[self.current] not in expected:
            return False

        self.current += 1
        return True

    def make_token(self, type, literal=None) -> Token:
        return Token(type, self.source[self.start:self.current], literal, self.line)

    def scan_number(self) -> Result[Token, str] | None:
        while self.peek().isdigit():
            self.advance()

        if self.peek() == '.' and self.peek(2).isdigit():
            self.advance()

            while self.peek().isdigit():
                self.advance()

        return Ok(self.make_token(TokenType.NUMBER, float(self.source[self.start:self.current])))

    def scan_identifier(self) -> Result[Token, str] | None:
        while self.peek().isalnum() or self.peek() == '_':
            self.advance()

        return Ok(self.make_token(
            RESERVED_KEYWORDS.get(self.source[self.start:self.current], TokenType.IDENTIFIER)))

    def scan_string(self, quote: str) -> Result[Token, str] | None:
        while self.peek() not in ['\0', quote]:
            if self.peek() == '\n':
                self.line += 1

            self.advance()

        if self.is_at_end():
            return Err(build_syntax_error(self, 'unterminated string'))

        self.advance()

        return Ok(self.make_token(
            TokenType.STRING,
            decode_escapes(self.source[self.start + 1:self.current - 1])))

    def scan_comment(self, comment: str) -> Result[None, str]:
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
                    return Err(build_syntax_error(self, 'unterminated multi-line comment'))

                self.advance()
                self.advance()

        return Ok(None)
