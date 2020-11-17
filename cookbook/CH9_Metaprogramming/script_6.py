"""
9.8. Defining decorators as part of a class

Problem: You want to define a decorator inside a class definition and apply it to
         other functions or methods
"""

from functools import wraps

class A:
    # decorator as an instance method
    def decorator1(self, func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            print("Decorator - 1")
            return func(*args, **kwargs)
        return wrapper

    # decorator as a class method
    @classmethod
    def decorator2(cls, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print("Decorator - 2")
            return func(*args, **kwargs)
        return wrapper


a = A()

@a.decorator1
def spam():
    print("spam...")
    pass

@A.decorator2
def grok():
    print("grok...")
    pass

spam()
grok()
