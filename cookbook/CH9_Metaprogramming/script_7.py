"""
9.9. Defining Decorator as classes

Problem: You want to wrap functions with a decorator, but the result is going to be
         a callable instance. You need your decorator to work both inside and outside
         class definitions.

Solution: to define a decorator as an instance, you need to make sure it implements
          the __call__() and __get__() methods. Ex. this code defines a class that puts
          a simple profiling layer around another function
"""

import types
from typing import Any
from functools import wraps

class Profiled:
    def __init__(self, func) -> None:
        wraps(func)(self)
        self.ncalls = 0

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self.ncalls += 1
        return self.__wrapped__(*args, **kwds)

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)

@Profiled
def add(x, y):
    return x + y

class Spam:
    @Profiled
    def bar(self, x):
        print(self, x)

add(2, 3)
add(4, 3)
add(4, 3)
add(4, 3)
add(4, 3)
print(add.ncalls)

s = Spam()
s.bar(1)
s.bar(2)
s.bar(3)
s.bar(4)
print(Spam.bar.ncalls)
