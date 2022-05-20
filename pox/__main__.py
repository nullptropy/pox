# coding: utf-8

import sys
import readline as _

from pox.scanner import Scanner

class Pox:
    def __init__(self):
        self.error_occured = False

    def run(self, source):
        print('\n'.join(map(str, self.tokenize(source))))
        return 65 if self.error_occured else 0

    def repl(self):
        while True:
            try:
                self.run(input('::: '))
            except (EOFError, KeyboardInterrupt) as _:
                return 0

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

    def tokenize(self, source):
        return Scanner(source).scan_tokens(self)

if __name__ == '__main__':
    exit(Pox().main())
