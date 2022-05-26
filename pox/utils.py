# coding: utf-8

import codecs
import numbers

def decode_escapes(s):
    return codecs.escape_decode(s)[0].decode()

def number(*operands):
    return all(map(lambda n: isinstance(n, numbers.Number), operands))

def stringify(obj):
    return 'nil' if obj is None else str(obj)
