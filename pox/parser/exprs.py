# coding: utf-8

from abc import ABC, abstractmethod

class Expr:
    pass

class Visitor(ABC):
    @abstractmethod
    def visit_binary_expr(self, expr):
        pass

    @abstractmethod
    def visit_grouping_expr(self, expr):
        pass

    @abstractmethod
    def visit_literal_expr(self, expr):
        pass

    @abstractmethod
    def visit_unary_expr(self, expr):
        pass

class Expr(Binary):
    def __init__(self, lt, op, rt):
        self.lt = lt
        self.op = op
        self.rt = rt

    def accept(self, visitor):
        return visitor.visit_binary_expr(self)

class Expr(Grouping):
    def __init__(self, expressions):
        self.expressions = expressions

    def accept(self, visitor):
        return visitor.visit_grouping_expr(self)

class Expr(Literal):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_literal_expr(self)

class Expr(Unary):
    def __init__(self, op, expression):
        self.op = op
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_unary_expr(self)
