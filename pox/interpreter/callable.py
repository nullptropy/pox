# coding: utf-8

from abc import ABC, abstractmethod

from .environment import Environment

class LoxCallable(ABC):
    @abstractmethod
    def arity(self):
        pass

    @abstractmethod
    def call(self, interpreter, arguments):
        pass

class LoxFunction(LoxCallable):
    def __init__(self, declaration):
        self.declaration = declaration

    def __str__(self):
        return f'<fn {self.declaration.name.lexeme}>'

    def arity(self):
        return len(self.declaration.params)

    def call(self, interpreter, arguments):
        environment = Environment(interpreter.globals)

        for i, param in enumerate(self.declaration.params):
            environment.define(param.lexeme, arguments[i])

        interpreter.execute_block(self.declaration.body, environment)
