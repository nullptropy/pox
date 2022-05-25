# coding: utf-8

import codecs
import numbers

SYNTAX_ERROR_TEMPLATE = '''\
  {line} | {line_text}
SyntaxError: {message}'''

def build_syntax_error(scanner, message, line=None):
    line = line if line else scanner.line

    return SYNTAX_ERROR_TEMPLATE.format(
        line=line,
        line_text=scanner.source.split('\n')[line - 1],
        message=message)

def build_parse_error(parser, message):
    return f'{parser.peek()}: {message}'

def decode_escapes(s):
    return codecs.escape_decode(s)[0].decode()

def number(*operands):
    return all(map(lambda n: isinstance(n, numbers.Number), operands))

def stringify(obj):
    if obj is None:
        return 'nil'

    return str(obj)
