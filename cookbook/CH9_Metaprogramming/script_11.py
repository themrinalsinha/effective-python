"""
9.15. Defining a metaclass that takes optional arguments

Problem: You want to define a metaclass that allows class definitions to supply optional
         arguments, possibly to control or configure aspects of processing during type creation.

Solution: When defining classes, Python allows a metaclass to be specified using metaclass
          keyword argument in the class statement.
"""
from abc import ABC, ABCMeta, abstractmethod

class IStream(metaclass=ABCMeta):
    @abstractmethod
    def read(self, maxsize=None):
        pass

    @abstractmethod
    def write(self, data):
        pass

class MyMeta(type):
    # optional
    @classmethod
    def __prepare__(cls, name, bases, *, debug=False, synchronize=False):
        # custom processing
        # ...
        return super().__prepare__(name, bases)

    # required
    def __new__(cls, name, bases, ns, *, debug=False, synchronize=False):
        # custom processing
        # ...
        return super().__new__(cls, name, bases, ns)

    # required
    def __init__(self, name, bases, ns, *, debug=False, synchronize=False) -> None:
        # custom processing
        super().__init__(name, bases, ns)


# # However, in custom metaclasses, additional keyword arguments can be supplied.
# class Spam(metaclass=MyMeta, debug=True, synchronize=True):
#     ....
class Spam(metaclass=MyMeta):
    debug = True
    synchronize = True
