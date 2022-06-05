# coding: utf-8

from pox.error import RuntimeError

class Environment:
    def __init__(self, enclosing=None):
        self.values = {}
        self.enclosing = enclosing

    def define(self, name, value): # name: str
        self.values[name] = value

    def ancestor(self, distance):
        environment = self

        for _ in range(distance):
            environment = environment.enclosing

        return environment

    def get(self, name): # name: Token
        if name.lexeme in self.values:
            return self.values[name.lexeme]

        if self.enclosing:
            return self.enclosing.get(name)

        raise RuntimeError(name, f'undefined variable {name.lexeme}')

    def get_at(self, distance, name): # name: str
        return self.ancestor(distance).values[name]

    def assign(self, name, value):
        if name.lexeme in self.values:
            return self.values.update({name.lexeme: value})

        if self.enclosing:
            return self.enclosing.assign(name, value)

        raise RuntimeError(name, f'undefined variable {name.lexeme}')

    def assign_at(self, distance, name, value):
        self.ancestor(distance).values.update({name.lexeme: value})
