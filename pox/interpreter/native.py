# coding: utf-8

from pox.utils import stringify
from pox.interpreter.callable import PoxCallable

class NativeFunction(PoxCallable):
    def __str__(self):
        return f'<native fn {self.name}>'

    def arity(self):
        pass

    def call(self, *_):
        pass

class PRINT(NativeFunction):
    name = 'print'

    def arity(self):
        return 1

    def call(self, _, arguments):
        print(stringify(arguments[0]))

class INPUT(NativeFunction):
    name = 'input'

    def arity(self):
        return 1

    def call(self, _, arguments):
        return input(arguments[0])

def init_native_functions(interpreter):
    for function in NativeFunction.__subclasses__():
        interpreter.globals.define(function.name, function())
