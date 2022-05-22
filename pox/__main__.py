# coding: utf-8

import sys
import readline as _

from pox.parser import Parser, Visitor, ParseError
from pox.scanner import Scanner, ScannerError

class ASTPrinter(Visitor):
    def visit_binary(self, expr):
        return f'({expr.op.lexeme} {expr.lt.accept(self)} {expr.rt.accept(self)})'

    def visit_grouping(self, expr):
        return f'(group {expr.expressions.accept(self)})'

    def visit_literal(self, expr):
        return str(expr.value) if expr.value else 'nil'

    def visit_unary(self, expr):
        return f'({expr.op.lexeme} {expr.expression.accept(self)})'

    def print(self, expression):
        print(expression.accept(self))

class Pox:
    def __init__(self):
        self.ast_printer = ASTPrinter()
        self.error_occured = False

    def run(self, source):
        tokens = self.tokenize(source)
        expression = Parser(tokens).parse()

        if self.error_occured:
            return 65

        return self.ast_printer.print(expression) or 0

    def tokenize(self, source):
        tokens  = []
        scanner = Scanner(source)

        while True:
            try:
                if token := scanner.scan_token():
                    tokens.append(token)
            except StopIteration:
                break
            except ScannerError as err:
                self.report_error(err)

        return tokens

    def parse(self, tokens):
        parser = Parser(tokens)

        try:
            return parser.parse()
        except ParseError as err:
            self.report_error(err)

    def report_error(self, error):
        print(error)
        self.error_occured = True

    def repl(self):
        while True:
            try:
                self.error_occured = False
                self.run(input('::: '))
            except (EOFError, KeyboardInterrupt) as _:
                return 0
            except Exception as err:
                print(err)

    def run_file(self, path):
        return self.run(open(path, 'r').read())

    def main(self):
        match len(sys.argv):
            case 1:
                return self.repl()
            case 2:
                return self.run_file(sys.argv[1])
            case _:
                return print("usage: pox [path]") or 64

if __name__ == '__main__':
    exit(Pox().main())
