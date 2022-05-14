# coding: utf-8

SYNTAX_ERROR_TEMPLATE = '''\
  {line} | {line_text}
SyntaxError: {message}'''

def build_syntax_error(scanner, message: str) -> str:
    return SYNTAX_ERROR_TEMPLATE.format(
        line=scanner.line,
        line_text=scanner.source.split('\n')[scanner.line - 1],
        message=message)

# TODO: implement this properly
def decode_escapes(s: str) -> str:
    for i, c in enumerate('abtnvfr'):
        s = s.replace(f'\\{c}', chr(7 + i))

    return s
