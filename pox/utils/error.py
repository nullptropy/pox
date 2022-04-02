# coding: utf-8

def build_syntax_error(scanner, message: str) -> str:
    return f'SyntaxError: {scanner.line} | {message}'
