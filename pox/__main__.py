# coding: utf-8

import sys
import readline as _

from pox.parser import Parser, ParseError
from pox.scanner import Scanner, ScannerError
from pox.interpreter import Interpreter, RuntimeError

class Pox:
    def __init__(self):
        self.error_occured = False
        self.runtime_error_occured = False

    def report_error(self, error):
        print(error)
        self.error_occured = True

    def repl(self):
        interpreter = Interpreter()

        while True:
            try:
                self.error_occured = False
                self.run(input('::: '), interpreter)
            except (EOFError, KeyboardInterrupt) as _:
                return 0
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
        expression = Parser(self.tokenize(source)).parse()

        if not self.error_occured:
            try:
                return print(interpreter.interpret(expression)) or 0
            except RuntimeError as err:
                self.runtime_error_occured = True
                self.report_error(err)

        return 70 if self.runtime_error_occured else 65

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

if __name__ == '__main__':
    exit(Pox().main())
