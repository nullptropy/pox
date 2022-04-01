# coding: utf-8

# TODO: implement this properly
def decode_escapes(s: str) -> str:
    for i, c in enumerate('abtnvfr'):
        s = s.replace(f'\\{c}', chr(7 + i))
    
    return s
