# coding: utf-8

from abc import ABC, abstractmethod
from .environment import Environment

from pox.error import RuntimeError

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class LoxCallable(ABC):
    @abstractmethod
    def arity(self):
        pass

    @abstractmethod
    def call(self, interpreter, arguments):
        pass

class LoxFunction(LoxCallable):
    def __init__(self, closure, declaration):
        self.closure = closure
        self.declaration = declaration

    def __str__(self):
        return f'<fn {self.declaration.name.lexeme}>'

    def arity(self):
        return len(self.declaration.params)

    def call(self, interpreter, arguments):
        environment = Environment(self.closure)

        for i, param in enumerate(self.declaration.params):
            environment.define(param.lexeme, arguments[i])

        try:
            interpreter.execute_block(self.declaration.body, environment)
        except ReturnException as return_value:
            return return_value.value

    def bind(self, instance):
        environment = Environment(self.closure)
        environment.define('this', instance)

        return LoxFunction(environment, self.declaration)

class LoxInstance:
    def __init__(self, pclass):
        self.fields = {}
        self.pclass = pclass

    def __str__(self):
        return f'<class instance {self.pclass.name}>'

    def get(self, name):
        if name.lexeme in self.fields:
            return self.fields[name.lexeme]

        if method := self.pclass.find_method(name.lexeme):
            return method.bind(self)

        raise RuntimeError(name, f'undefined property \'{name.lexeme}\'')

    def set(self, name, value):
        self.fields.update({name.lexeme: value})

class LoxClass(LoxCallable):
    def __init__(self, name, methods):
        self.name = name
        self.methods = methods

    def __str__(self):
        return f'<class {self.name}>'

    def find_method(self, name):
        return self.methods.get(name)

    def arity(self):
        return 0

    def call(self, interpreter, arguments):
        return LoxInstance(self)
