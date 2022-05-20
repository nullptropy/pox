# pox

lox programming language ast-walking interpreter

**Note:** some differences compared to the original implementation of lox
- strings can be denoted with single quotes
- nesting string quotes is legal, `'string \'literal\' nice'`, `"string \"literal\" nice"`
- `/* multi-line comments (nesting them is not supported) */`
