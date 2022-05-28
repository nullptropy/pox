# coding: utf-8

from abc import ABC, abstractmethod

class Expr:
    pass

class ExprVisitor(ABC):
    @abstractmethod
    def visit_binary_expr(self, expr):
        pass

    @abstractmethod
    def visit_call_expr(self, expr):
        pass

    @abstractmethod
    def visit_grouping_expr(self, expr):
        pass

    @abstractmethod
    def visit_literal_expr(self, expr):
        pass

    @abstractmethod
    def visit_logical_expr(self, expr):
        pass

    @abstractmethod
    def visit_unary_expr(self, expr):
        pass

    @abstractmethod
    def visit_variable_expr(self, expr):
        pass

    @abstractmethod
    def visit_assign_expr(self, expr):
        pass

class Binary(Expr):
    def __init__(self, lt, op, rt):
        self.lt = lt
        self.op = op
        self.rt = rt

    def accept(self, visitor):
        return visitor.visit_binary_expr(self)

class Call(Expr):
    def __init__(self, callee, paren, arguments):
        self.callee = callee
        self.paren = paren
        self.arguments = arguments

    def accept(self, visitor):
        return visitor.visit_call_expr(self)

class Grouping(Expr):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_grouping_expr(self)

class Literal(Expr):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_literal_expr(self)

class Logical(Expr):
    def __init__(self, lt, op, rt):
        self.lt = lt
        self.op = op
        self.rt = rt

    def accept(self, visitor):
        return visitor.visit_logical_expr(self)

class Unary(Expr):
    def __init__(self, op, expression):
        self.op = op
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_unary_expr(self)

class Variable(Expr):
    def __init__(self, name):
        self.name = name

    def accept(self, visitor):
        return visitor.visit_variable_expr(self)

class Assign(Expr):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def accept(self, visitor):
        return visitor.visit_assign_expr(self)
