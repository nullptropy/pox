#!/usr/bin/env python3
# coding: utf-8

# TODO: come up with something better
# when i feel like doing so

FILE_HEADER = '''\
# coding: utf-8

from abc import ABC, abstractmethod

from typing import Any
from pox.scanner import Token

class Expr:
    pass
'''

PARAM_TEMPLATE = '{1}: {0}'
ASSGN_TEMPLATE = ' ' * 8 + 'self.{0} = {0}'
EXPRS_TEMPLATE = '''\
class {0}(Expr):
    def __init__(self, {1}):
{2}

    def accept(self, visitor):
        return visitor.visit_{3}(self)
\
'''

VISITOR_TEMPLATE = '''\
class Visitor(ABC):
{}\
'''
VISIT_TEMPLATE = '''\
    @abstractmethod
    def visit_{0}(self, expr):
        pass
'''

def generate_expr_class(name, *fields):
    params = ', '.join(PARAM_TEMPLATE.format(*f.split(' ')) for f in fields)
    fields = '\n'.join(ASSGN_TEMPLATE.format(f.split(' ')[1]) for f in fields)

    return EXPRS_TEMPLATE.format(name, params, fields, name.lower())

def generate_exprs_file(expressions):
    visits = '\n'.join(VISIT_TEMPLATE.format(expr[0].lower()) for expr in expressions)

    print(
        FILE_HEADER + '\n' + VISITOR_TEMPLATE.format(visits) + '\n' +
        '\n'.join(generate_expr_class(n, *f) for n, *f in expressions), end='')

def main():
    generate_exprs_file([
        ['Binary', 'Expr lt', 'Token op', 'Expr rt'],
        ['Grouping', 'Expr expressions'],
        ['Literal', 'Any value'],
        ['Unary', 'Token op', 'Expr expression'],
    ])

if __name__ == '__main__':
    main()
