# coding: utf-8

from abc import ABC, abstractmethod

class LoxCallable(ABC):
    @abstractmethod
    def arity(self):
        pass

    @abstractmethod
    def call(self, interpreter, arguments):
        pass
