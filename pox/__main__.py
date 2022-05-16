# coding: utf-8

import sys
import readline as _

from pox.scanner import Scanner

class Pox:
    def __init__(self):
        self.error_occured = False

    def run(self, source):
        tokens = self.tokenize(source)
        return 65 if self.error_occured else 0

    def repl(self):
        while True:
            try:
                self.tokenize(input('::: '))
            except (EOFError, KeyboardInterrupt) as _:
                return

    def run_file(self, path):
        return self.run(open(path, 'r').read())

    def main(self):
        match len(sys.argv):
            case 1:
                return self.repl() or 0
            case 2:
                return self.run_file(sys.argv[1])
            case _:
                return print("usage: pox [path]") or 64

    def tokenize(self, source):
        tokens = Scanner(source).scan_tokens()

        for token in tokens:
            print(token)

        return tokens

if __name__ == '__main__':
    exit(Pox().main())
