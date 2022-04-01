# coding: utf-8

import sys

from .utils import error
from .scanner import Token, Scanner

from result import Ok, Err 

class Pox:
    def __init__(self):
        self.error_occured = False

    def run(self, source: str) -> int:
        tokens = self.tokenize(source)

        return 65 if self.error_occured else 0

    def repl(self):
        pass

    def run_file(self, path: str) -> int:
        return self.run(open(path, 'r').read())

    def main(self) -> int:
        match len(sys.argv):
            case 1:
                return self.repl() or 0
            case 2:
                return self.run_file(sys.argv[1])
            case _:
                return print("usage: pox [path]") or 64

    def tokenize(self, source: str) -> list[Token]:
        tokens = []

        for token in Scanner(source):
            match token:
                case Ok(token):
                    print(token)
                    tokens.append(token)
                case Err(message):
                    self.error_occured = True
                    print(error.build_syntax_error(message))

        return tokens

if __name__ == '__main__':
    exit(Pox().main())
