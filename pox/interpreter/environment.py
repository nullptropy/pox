# coding: utf-8

from pox.error import RuntimeError

class Environment:
    def __init__(self, enclosing=None):
        self.values = {}
        self.enclosing = enclosing

    def define(self, name, value): # name: str
        self.values[name] = value

    def get(self, name): # name: Token
        if name.lexeme in self.values:
            return self.values[name.lexeme]

        if self.enclosing:
            return self.enclosing.get(name)

        raise RuntimeError(name, f'undefined variable {name.lexeme}')

    def assign(self, name, value):
        if name.lexeme in self.values:
            return self.values.update({name.lexeme: value})

        if self.enclosing:
            return self.assign(name, value)

        raise RuntimeError(name, f'undefined variable {name.lexeme}')
