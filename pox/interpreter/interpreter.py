# coding: utf-8

from pox.error import RuntimeError
from pox.utils import number, stringify

from pox.scanner import TokenType
from pox.parser import ExprVisitor, StmtVisitor

from .callable import LoxCallable, LoxFunction, ReturnException
from .environment import Environment

def check_number_operands(operator, *operands):
    if not number(*operands):
        raise RuntimeError(operator, 'operands must be numbers')

class Interpreter(ExprVisitor, StmtVisitor):
    def __init__(self):
        self.globals = Environment()
        self.environment = self.globals

    def evaluate(self, expr):
        return expr.accept(self)

    def interpret(self, stmts, pox):
        try:
            for stmt in stmts:
                self.execute(stmt)
        except RuntimeError as err:
            pox.report_error(err)

    def execute(self, stmt):
        return stmt.accept(self)

    def execute_block(self, stmts, env):
        previous = self.environment

        try:
            self.environment = env

            for stmt in stmts.statements:
                if stmt:
                    self.execute(stmt)
        finally:
            self.environment = previous

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

    def visit_logical_expr(self, expr):
        lt = self.evaluate(expr.lt)

        if expr.op.type == TokenType.OR:
            if bool(lt): return lt
        else:
            if not bool(lt): return lt

        return self.evaluate(expr.rt)

    def visit_unary_expr(self, expr):
        right = self.evaluate(expr.expression)

        match expr.op.type:
            case TokenType.BANG:
                return not bool(right)
            case TokenType.MINUS:
                check_number_operands(expr.op, right)
                return -right

    def visit_call_expr(self, expr):
        function  = self.evaluate(expr.callee)
        arguments = list(map(self.evaluate, expr.arguments))

        if not isinstance(function, LoxCallable):
            raise RuntimeError(expr.paren, 'can only call functions and classes')

        if len(arguments) != function.arity():
            raise RuntimeError(
                expr.paren,
                f'expected {function.arity()} arguments but got {len(arguments)}')

        return function.call(self, arguments)

    def visit_variable_expr(self, expr):
        return self.environment.get(expr.name)

    def visit_assign_expr(self, expr):
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value

    def visit_function_stmt(self, stmt):
        self.environment.define(stmt.name.lexeme, LoxFunction(stmt))

    def visit_if_stmt(self, stmt):
        if bool(self.evaluate(stmt.condition)):
            self.execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self.execute(stmt.else_branch)

    def visit_block_stmt(self, stmt):
        self.execute_block(stmt, Environment(self.environment))

    def visit_var_stmt(self, stmt):
        self.environment.define(
            stmt.name.lexeme,
            self.evaluate(stmt.initializer) if stmt.initializer else None)

    def visit_expression_stmt(self, stmt):
        self.evaluate(stmt.expression)

    def visit_while_stmt(self, stmt):
        while bool(self.evaluate(stmt.condition)):
            self.execute(stmt.body)

    def visit_print_stmt(self, stmt):
        print(stringify(self.evaluate(stmt.expression)))

    def visit_return_stmt(self, stmt):
        raise ReturnException(self.evaluate(stmt.value) if stmt.value else None)
