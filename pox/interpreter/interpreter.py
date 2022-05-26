# coding: utf-8

from pox.utils import number, stringify
from pox.parser import Visitor
from pox.scanner import TokenType

class RuntimeError(Exception):
    def __init__(self, token, message):
        self.token = token
        self.message = message

def check_number_operands(operator, *operands):
    if not number(*operands):
        raise RuntimeError(operator, 'operands must be numbers')

class Interpreter(Visitor):
    def evaluate(self, expr):
        return expr.accept(self)

    def interpret(self, expression):
        return stringify(self.evaluate(expression))

    def visit_binary_expr(self, expr):
        lt = self.evaluate(expr.lt)
        rt = self.evaluate(expr.rt)

        if expr.op.type not in [TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL, TokenType.PLUS]:
            check_number_operands(expr.op, lt, rt)

        match expr.op.type:
            case TokenType.MINUS:         return lt  - rt
            case TokenType.STAR:          return lt  * rt
            case TokenType.LESS:          return lt  < rt
            case TokenType.GREATER:       return lt  > rt
            case TokenType.LESS_EQUAL:    return lt <= rt
            case TokenType.GREATER_EQUAL: return lt >= rt
            case TokenType.EQUAL_EQUAL:   return lt == rt
            case TokenType.BANG_EQUAL:    return not (lt == rt)
            case TokenType.SLASH:
                if rt == 0:
                    raise RuntimeError(expr.op, 'division by zero')

                return lt  / rt
            case TokenType.PLUS:
                try:
                    if isinstance(lt, str) or isinstance(rt, str):
                        return f'{lt}{rt}'

                    return lt + rt
                except TypeError:
                    raise RuntimeError(expr.op, 'operands must be numbers or strings')

    def visit_grouping_expr(self, expr):
        return self.evaluate(expr.expression)

    def visit_literal_expr(self, expr):
        return expr.value

    def visit_unary_expr(self, expr):
        right = self.evaluate(expr.expression)

        match expr.op.type:
            case TokenType.BANG:
                return not bool(right)
            case TokenType.MINUS:
                check_number_operands(expr.op, right)
                return -right
