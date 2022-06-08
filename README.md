# pox

[lox programming language](https://craftinginterpreters.com/) ast-walking interpreter

**Note:** some differences compared to the original implementation of lox
- strings can be denoted with single quotes
- `/* multi-line comments (nesting them is not supported) */`
- escape sequences supported by [python](https://github.com/python/cpython/blob/f62ad4f2c4214fdc05cc45c27a5c068553c7942c/Objects/bytesobject.c#L1062) are supported on pox as well
- truthiness is implemented with python's [bool](https://docs.python.org/3/library/functions.html#bool) function ([truth testing procedure](https://docs.python.org/3/library/stdtypes.html#truth))
- `fn` instead of `fun`
- `let` instead of `var`

TODO: write some tests D:
