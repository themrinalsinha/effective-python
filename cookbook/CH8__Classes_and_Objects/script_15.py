"""
8.20. calling a method on an object given the name as a string

Problem: you have the name of a method that you want to call on an object stored
         in a string and you want to execute the method.
"""

import math

class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f'Point({self.x}, {self.y})'

    def distance(self, x, y):
        return math.hypot(self.x - x, self.y - y)

p = Point(2, 3)
d = getattr(p, 'distance')(0, 0)

# An alternate approach is to use operator.methodcaller() eg:
import operator
d = operator.methodcaller('distance', 0, 0)(p)

