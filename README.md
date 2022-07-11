# pox

[lox programming language](https://craftinginterpreters.com/) ast-walking interpreter

**Note:** some differences compared to the original implementation of lox
- strings can be denoted with single quotes
- `/* multi-line comments (nesting them is not supported) */`
- escape sequences supported by [python](https://github.com/python/cpython/blob/f62ad4f2c4214fdc05cc45c27a5c068553c7942c/Objects/bytesobject.c#L1062) are supported on pox as well
- truthiness is implemented with python's [bool](https://docs.python.org/3/library/functions.html#bool) function ([truth testing procedure](https://docs.python.org/3/library/stdtypes.html#truth))
- `fn` instead of `fun`
- `let` instead of `var`
- pox has support for else-if (see the examples folder)
- the `print` statement doesn't exist

**built-in classes**:
- [`list`](https://github.com/brkp/pox/blob/main/pox/interpreter/native.py#L184) this is a really thin wrapper around python's list type, see the source code for methods it has

[**built-in functions**](https://github.com/fxxf/pox/blob/main/pox/interpreter/native.py):
- `print(value)` prints the given value to stdout without a trailing new line
- `println(value)` prints the given value to stdout with a trailing new line
- `input(prompt)` [python's input function](https://docs.python.org/3/library/functions.html#input), returns `nil` on `EOFError`
- `chr(int), ord(char)` python's [chr](https://docs.python.org/3/library/functions.html#chr) and [ord](https://docs.python.org/3/library/functions.html#ord) functions, they both return `nil` on `TypeError`
- `str(object), int(string), float(string)` python's [str](https://docs.python.org/3/library/functions.html#str), [int](https://docs.python.org/3/library/functions.html#int) and [float](https://docs.python.org/3/library/functions.html#float) functions. `int` and `float` returns `nil` on `ValueError`
- `strlen(string)` returns the length of a given string, `nil` if the passed argument is not a string
- `strn(string, n)` returns the nth char of a given string, `nil` if n > len(string) or if `string` is not a string
- `exit(value)` calls [sys.exit](https://docs.python.org/3/library/sys.html#sys.exit) with the given `value`
- `time()` returns the time in seconds since the epoch as a floating point number 
- `sleep(secs)` suspend execution of the program for the given number of seconds
- `pow(a, b)` returns `a**b`
