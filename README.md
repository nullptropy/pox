# pox

lox programming language ast-walking interpreter

**Note:** some differences compared to the original implementation of lox
- strings can be denoted with single quotes
- nesting string quotes is legal, `'string \'literal\' nice'`, `"string \"literal\" nice"`
- `/* multi-line comments (nesting them is not supported) */`
- escape sequences supported by [python](https://github.com/python/cpython/blob/f62ad4f2c4214fdc05cc45c27a5c068553c7942c/Objects/bytesobject.c#L1062) are supported on pox as well
