" Lox syntax file
" Language: Lox
" Maintainer: Timmy Jose

:if exists("b:current_syntax")
:  finish
:endif

" keywords
:syntax keyword poxKeyword class fn let this
:syntax keyword poxKeyword for while return

" booleans
:syntax keyword poxBoolean true false

" constants
:syntax keyword poxConstant nil

" functions
:syntax keyword poxFunction print println input chr ord
:syntax keyword poxFunction str int float strlen strn
:syntax keyword poxFunction exit time sleep

" operators
:syntax match poxOperator "\v\*"
:syntax match poxOperator "\v\+"
:syntax match poxOperator "\v\-"
:syntax match poxOperator "\v/"
:syntax match poxOperator "\v\="
:syntax match poxOperator "\v!"

" conditionals
:syntax keyword poxConditional if else and or else

" numbers
:syntax match poxNumber "\v\-?\d*(\.\d+)?"

" strings
:syntax region poxString start="\v\"" end="\v\""
:syntax region poxString start="\v'" end="\v'"

" comments
:syntax match poxComment "\v//.*$"

:highlight link poxKeyword Keyword
:highlight link poxBoolean Boolean
:highlight link poxConstant Constant
:highlight link poxFunction Function
:highlight link poxOperator Operator
:highlight link poxConditional Conditional
:highlight link poxNumber Number
:highlight link poxString String
:highlight link poxComment Comment

:let b:current_syntax = "pox"
