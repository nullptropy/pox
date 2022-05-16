# coding: utf-8

from abc import ABC, abstractmethod

class Expr:
    pass

class Visitor(ABC):
    @abstractmethod
    def visit_binary(self, expr):
        pass

    @abstractmethod
    def visit_grouping(self, expr):
        pass

    @abstractmethod
    def visit_literal(self, expr):
        pass

    @abstractmethod
    def visit_unary(self, expr):
        pass

class Binary(Expr):
    def __init__(self, lt, op, rt):
        self.lt = lt
        self.op = op
        self.rt = rt

    def accept(self, visitor):
        return visitor.visit_binary(self)

class Grouping(Expr):
    def __init__(self, expressions):
        self.expressions = expressions

    def accept(self, visitor):
        return visitor.visit_grouping(self)

class Literal(Expr):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_literal(self)

class Unary(Expr):
    def __init__(self, op, expression):
        self.op = op
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_unary(self)
