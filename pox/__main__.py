# coding: utf-8

import sys
import readline as _

from pox.scanner import Scanner
from pox.parser import Parser, Resolver
from pox.interpreter import Interpreter, RuntimeError

class Pox:
    def __init__(self):
        self.error_occured = False
        self.runtime_error_occured = False

    def report_error(self, error):
        print(error)

        if isinstance(error, RuntimeError):
            self.runtime_error_occured = True
            return

        self.error_occured = True

    def repl(self):
        interpreter = Interpreter()

        while True:
            try:
                self.error_occured = False
                self.run(input('::: '), interpreter)
            except EOFError:
                return 0
            except KeyboardInterrupt:
                print()
            except Exception as err:
                print(err)

    def run_file(self, path):
        return self.run(open(path, 'r').read(), Interpreter())

    def main(self):
        match len(sys.argv):
            case 1:
                return self.repl()
            case 2:
                return self.run_file(sys.argv[1])
            case _:
                return print("usage: pox [path]") or 64

    def run(self, source, interpreter):
        statements = self.parse(self.tokenize(source))

        if not self.error_occured:
            resolver = Resolver(self, interpreter)
            resolver.resolve(*statements)

        if not self.error_occured:
            interpreter.interpret(statements, self)

        if self.error_occured:
            return 65

        return 70 if self.runtime_error_occured else 0

    def tokenize(self, source):
        return Scanner(source).scan_tokens(self)

    def parse(self, tokens):
        return Parser(tokens).parse(self)

if __name__ == '__main__':
    exit(Pox().main())
