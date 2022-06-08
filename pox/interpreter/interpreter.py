# coding: utf-8

from pox.error import RuntimeError
from pox.utils import number, stringify

from pox.scanner import TokenType
from pox.parser import ExprVisitor, StmtVisitor

from .callable import *
from .environment import Environment

def check_number_operands(operator, *operands):
    if not number(*operands):
        raise RuntimeError(operator, 'operands must be numbers')

class Interpreter(ExprVisitor, StmtVisitor):
    def __init__(self):
        self.locals = {}
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

    def resolve(self, expr, depth):
        self.locals[expr] = depth

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

    def look_up_variable(self, name, expr):
        if (distance := self.locals.get(expr)) is not None:
            return self.environment.get_at(distance, name.lexeme)

        return self.globals.get(name)

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

    def visit_get_expr(self, expr):
        object = self.evaluate(expr.object)

        if isinstance(object, LoxInstance):
            return object.get(expr.name)

        raise RuntimeError(expr.name, 'only instances have properties')

    def visit_literal_expr(self, expr):
        return expr.value

    def visit_logical_expr(self, expr):
        lt = self.evaluate(expr.lt)

        if expr.op.type == TokenType.OR:
            if bool(lt): return lt
        else:
            if not bool(lt): return lt

        return self.evaluate(expr.rt)

    def visit_set_expr(self, expr):
        object = self.evaluate(expr.object)

        if not isinstance(object, LoxInstance):
            raise RuntimeError(expr.name, 'only instances have fields')

        value = self.evaluate(expr.value)
        object.set(expr.name, value)

        return value

    def visit_super_expr(self, expr):
        distance = self.locals.get(expr)

        superclass = self.environment.get_at(distance, 'super')
        object = self.environment.get_at(distance - 1, 'this')

        if method := superclass.find_method(expr.method.lexeme):
            return method.bind(object)

        raise RuntimeError(expr.method, f'undefined property {expr.method.lexeme}')

    def visit_this_expr(self, expr):
        return self.look_up_variable(expr.keyword, expr)

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
        return self.look_up_variable(expr.name, expr)

    def visit_assign_expr(self, expr):
        value = self.evaluate(expr.value)

        if distance := self.locals.get(expr):
            return self.environment.assign_at(distance, expr.name, value) or value

        return self.globals.assign(expr.name, value) or value

    def visit_function_stmt(self, stmt):
        self.environment.define(
            stmt.name.lexeme, LoxFunction(self.environment, stmt, False))

    def visit_if_stmt(self, stmt):
        if bool(self.evaluate(stmt.condition)):
            self.execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self.execute(stmt.else_branch)

    def visit_block_stmt(self, stmt):
        self.execute_block(stmt, Environment(self.environment))

    def visit_class_stmt(self, stmt):
        if superclass := stmt.superclass:
            superclass = self.evaluate(superclass)

            if not isinstance(superclass, LoxClass):
                raise RuntimeError(
                    stmt.superclass.name, '`superclass` must be a class')

        self.environment.define(stmt.name.lexeme, None)

        if stmt.superclass:
            self.environment = Environment(self.environment)
            self.environment.define('super', superclass)

        methods = {}
        for method in stmt.methods:
            name = method.name.lexeme
            methods.update({
                name: LoxFunction(self.environment, method, name == 'init')})

        if stmt.superclass:
            self.environment = self.environment.enclosing

        self.environment.assign(
            stmt.name, LoxClass(stmt.name.lexeme, superclass, methods))

    def visit_let_stmt(self, stmt):
        self.environment.define(
            stmt.name.lexeme,
            self.evaluate(stmt.initializer) if stmt.initializer else None)

    def visit_expression_stmt(self, stmt):
        self.evaluate(stmt.expression)

    def visit_while_stmt(self, stmt):
        while bool(self.evaluate(stmt.condition)):
            self.execute(stmt.body)

    def visit_return_stmt(self, stmt):
        raise ReturnException(self.evaluate(stmt.value) if stmt.value else None)
