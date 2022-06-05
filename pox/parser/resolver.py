# coding: utf-8

from pox.parser.exprs import *
from pox.parser.stmts import *
from pox.error import ResolveError

from enum import Enum, auto

class FunctionType(Enum):
    NONE = auto()
    METHOD = auto()
    FUNCTION = auto()

class ClassType(Enum):
    NONE = auto()
    CLASS = auto()

class Resolver(ExprVisitor, StmtVisitor):
    def __init__(self, pox, interpreter):
        self.scopes = []

        self.curr_fn = FunctionType.NONE
        self.curr_cl = ClassType.NONE

        self.pox = pox
        self.interpreter = interpreter

    def resolve(self, *args):
        for n in args:
            n.accept(self)

    def resolve_local(self, expr, name):
        for i in range(0, len(self.scopes))[::-1]:
            if name.lexeme in self.scopes[i]:
                return self.interpreter.resolve(expr, len(self.scopes) - 1 - i)

    def resolve_function(self, function, fn_type):
        enclosing_fn = self.curr_fn
        self.curr_fn = fn_type
        self.begin_scope()

        for param in function.params:
            self.declare(param)
            self.define(param)

        self.resolve(*function.body.statements)
        self.end_scope()
        self.curr_fn = enclosing_fn

    def begin_scope(self):
        self.scopes.append({})

    def end_scope(self):
        self.scopes.pop()

    def declare(self, name):
        if not self.scopes:
            return None

        if name.lexeme in self.scopes[-1]:
            self.pox.report_error(
                ResolveError(name, 'there already is a variable with this name in this scope'))

        self.scopes[-1][name.lexeme] = False

    def define(self, name):
        if not self.scopes:
            return None

        self.scopes[-1][name.lexeme] = True

    def visit_binary_expr(self, expr):
        self.resolve(expr.lt)
        self.resolve(expr.rt)

    def visit_call_expr(self, expr):
        self.resolve(expr.callee)

        for arg in expr.arguments:
            self.resolve(arg)

    def visit_grouping_expr(self, expr):
        self.resolve(expr.expression)

    def visit_get_expr(self, expr):
        self.resolve(expr.object)

    def visit_literal_expr(self, _):
        pass

    def visit_logical_expr(self, expr):
        self.resolve(expr.lt)
        self.resolve(expr.rt)

    def visit_set_expr(self, expr):
        self.resolve(expr.object)
        self.resolve(expr.value)

    def visit_this_expr(self, expr):
        if self.curr_cl == ClassType.NONE:
            return self.pox.report_error(
                ResolveError(expr.keyword, 'can\'t use \'this\' outside of a class'))

        self.resolve_local(expr, expr.keyword)

    def visit_unary_expr(self, expr):
        self.resolve(expr.expression)

    def visit_variable_expr(self, expr):
        if self.scopes and self.scopes[-1].get(expr.name.lexeme) == False:
            self.pox.report_error(
                ResolveError(expr.name, 'can\'t read local variable in its own initializer'))

        self.resolve_local(expr, expr.name)

    def visit_assign_expr(self, expr):
        self.resolve(expr.value)
        self.resolve_local(expr, expr.name)

    def visit_block_stmt(self, stmt):
        self.begin_scope()
        self.resolve(*stmt.statements)
        self.end_scope()

    def visit_class_stmt(self, stmt):
        enclosing_cl = self.curr_cl
        self.curr_cl = ClassType.CLASS

        self.declare(stmt.name)
        self.define(stmt.name)

        self.begin_scope()
        self.scopes[-1].update({'this': True})

        for method in stmt.methods:
            self.resolve_function(method, FunctionType.METHOD)

        self.end_scope()
        self.curr_cl = enclosing_cl

    def visit_var_stmt(self, stmt):
        self.declare(stmt.name)

        if stmt.initializer:
            self.resolve(stmt.initializer)

        self.define(stmt.name)

    def visit_function_stmt(self, stmt):
        self.declare(stmt.name)
        self.define(stmt.name)

        self.resolve_function(stmt, FunctionType.FUNCTION)

    def visit_expression_stmt(self, stmt):
        self.resolve(stmt.expression)

    def visit_if_stmt(self, stmt):
        self.resolve(stmt.condition)
        self.resolve(stmt.then_branch)

        if stmt.else_branch:
            self.resolve(stmt.else_branch)

    def visit_print_stmt(self, stmt):
        self.resolve(stmt.expression)

    def visit_return_stmt(self, stmt):
        if self.curr_fn == FunctionType.NONE:
            self.pox.report_error(
                ResolveError(stmt.keyword, 'can\'t return from top-level code'))

        if stmt.value:
            self.resolve(stmt.value)

    def visit_while_stmt(self, stmt):
        self.resolve(stmt.condition)
        self.resolve(stmt.body)
