# coding: utf-8

SYNTAX_ERROR_TEMPLATE = '''\
  {line} | {line_text}
SyntaxError: {message}'''

class ScannerError(Exception):
    pass

class ParseError(Exception):
    pass

class RuntimeError(Exception):
    def __init__(self, token, message):
        self.token = token
        self.message = message

def build_syntax_error(scanner, message, line=None):
    line = line if line else scanner.line

    return SYNTAX_ERROR_TEMPLATE.format(
        line=line,
        line_text=scanner.source.split('\n')[line - 1],
        message=message)

def build_parse_error(parser, message):
    return f'{parser.peek()}: {message}'

