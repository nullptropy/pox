# coding: utf-8

def build_syntax_error(scanner, message: str) -> str:
    return f'SyntaxError: {scanner.line} | {message}'

# TODO: implement this properly
def decode_escapes(s: str) -> str:
    for i, c in enumerate('abtnvfr'):
        s = s.replace(f'\\{c}', chr(7 + i))

    return s
