"""
9.19. Initializing class members at definition time

Problem: You want to initialize parts of a class definition once at the time a class
         is defined, not when instances are created.

Solution: Performing initialization or setup actions at the time of class definition is
          a classic use of metaclasses. Essentially, a metaclass is triggered at the point
          of a definition, at which point you can perform additional steps.
"""

import operator

class StructTupleMeta(type):
    def __init__(cls, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for n, name in enumerate(cls._fields):
            setattr(cls, name, property(operator.itemgetter(n)))

class StructTuple(tuple, metaclass=StructTupleMeta):
    _fields = []
    def __new__(cls, *args):
        if len(args) != len(cls._fields):
            raise ValueError(f"{len(cls._fields)} arguments required..")
        return super().__new__(cls, args)

class Stock(StructTuple):
    _fields = ['name', 'shares', 'price']

class Point(StructTuple):
    _fields = ['x', 'y']

s = Stock("ACME", 50, 91.1)
print(s)
