# coding: utf-8

from pox.error import RuntimeError

class Environment:
    def __init__(self):
        self.values = {}

    def define(self, name, value): # name: str
        self.values[name] = value

    def get(self, name): # name: Token
        if name.lexeme in self.values:
            return self.values[name.lexeme]

        raise RuntimeError(name, f'undefined variable {name.lexeme}')
