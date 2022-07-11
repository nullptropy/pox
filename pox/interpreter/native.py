# coding: utf-8

import sys
import time

from pox.utils import stringify
from pox.interpreter.callable import PoxCallable, PoxClass, PoxInstance

class NativeFunction(PoxCallable):
    name = None

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
        print(stringify(arguments[0]), end='')

class PRINTLN(NativeFunction):
    name = 'println'

    def arity(self):
        return 1

    def call(self, _, arguments):
        print(stringify(arguments[0]))

class INPUT(NativeFunction):
    name = 'input'

    def arity(self):
        return 1

    def call(self, _, arguments):
        try:
            return input(arguments[0])
        except EOFError:
            return None

class CHR(NativeFunction):
    name = 'chr'

    def arity(self):
        return 1

    def call(self, _, arguments):
        try:
            return chr(arguments[0])
        except Exception:
            return None

class ORD(NativeFunction):
    name = 'ord'

    def arity(self):
        return 1

    def call(self, _, arguments):
        try:
            return ord(arguments[0])
        except Exception:
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
        except Exception:
            return None

class FLOAT(NativeFunction):
    name = 'float'

    def arity(self):
        return 1

    def call(self, _, arguments):
        try:
            return float(arguments[0])
        except Exception:
            return None

class TIME(NativeFunction):
    name = 'time'

    def arity(self):
        return 0

    def call(self, *_):
        return time.time()

class SLEEP(NativeFunction):
    name = 'sleep'

    def arity(self):
        return 1

    def call(self, _, arguments):
        try:
            time.sleep(arguments[0])
        except Exception:
            pass

class EXIT(NativeFunction):
    name = 'exit'

    def arity(self):
        return 1

    def call(self, _, arguments):
        sys.exit(arguments[0])

def list_fn_wrapper(self, fn):
    def _fn(*args, **kwargs):
        try:
            return fn(self, *args, **kwargs)
        except:
            return False

    return _fn

class ListFn(PoxCallable):
    def __init__(self, name, arity, list):
        self.name = name
        self.list = list
        self._arity = arity

    def __str__(self):
        return f'<fn {self.name}>'

    def arity(self):
        return self._arity

    def call(self, *_):
        pass

class ListInstance(PoxInstance):
    functions = [
        (1, 'get', lambda s, _, a: s.list.data[a[0]]),
        (1, 'add', lambda s, _, a: s.list.data.append(a[0])),
        (1, 'pop', lambda s, _, a: s.list.data.pop(a[0])),
        (2, 'set', lambda s, _, a: s.list.data.__setitem__(*a)),
        (0, 'len', lambda s,   *_: len(s.list.data))]

    def __init__(self, pclass):
        self.data = []
        self.func = {}

        for (a, n, c) in self.functions:
            self.func[n] = ListFn(n, a, self)
            self.func[n].call = list_fn_wrapper(self.func[n], c)

        super().__init__(pclass)

    def get(self, name):
        if fn := self.func.get(name.lexeme):
            return fn

        return super().get(name)

class LIST(PoxClass):
    def __init__(self):
        super().__init__('list', None, {})

    def call(self, *_):
        return ListInstance(self)

def init_native_functions(interpreter):
    for function in NativeFunction.__subclasses__():
        interpreter.globals.define(function.name, function())

    interpreter.globals.define('list', LIST())
