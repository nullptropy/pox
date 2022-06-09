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

class CHR(NativeFunction):
    name = 'chr'

    def arity(self):
        return 1

    def call(self, _, arguments):
        try:
            return chr(arguments[0])
        except TypeError:
            return None

class ORD(NativeFunction):
    name = 'ord'

    def arity(self):
        return 1

    def call(self, _, arguments):
        try:
            return ord(arguments[0])
        except TypeError:
            return None

class STR(NativeFunction):
    name = 'str'

    def arity(self):
        return 1

    def call(self, _, arguments):
        return str(arguments[0])

class STRN(NativeFunction):
    name = 'strn'

    def arity(self):
        return 2

    def call(self, _, arguments):
        string, index = arguments

        if isinstance(string, str) and index < len(string):
            return string[index]

class STRLEN(NativeFunction):
    name = 'strlen'

    def arity(self):
        return 1

    def call(self, _, arguments):
        if isinstance(arguments[0], str):
            return len(arguments[0])

class INT(NativeFunction):
    name = 'int'

    def arity(self):
        return 1

    def call(self, _, arguments):
        try:
            return int(arguments[0])
        except ValueError:
            return None

class FLOAT(NativeFunction):
    name = 'float'

    def arity(self):
        return 1

    def call(self, _, arguments):
        try:
            return float(arguments[0])
        except ValueError:
            return None

def init_native_functions(interpreter):
    for function in NativeFunction.__subclasses__():
        interpreter.globals.define(function.name, function())
