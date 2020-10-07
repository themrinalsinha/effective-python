"""
One of the most important mantras of software development is "Don't repeat yourself".
That is, any time you are facing problem with creating highly repetitive code, it often
pays to look for a more elegant solution. In Python, such problems are often solved under
the category of "metaprogramming"

In a nutshell, metagrogramming is about creating functions and classes whose main goal is
to manipulate code (eg. modifying, generating or wrapping existing code).

Main features include:
- decorators
- class decorators
- metaclasses
and other useful topics -- including signature objects, execution of code with exec() and
inspecting the internals of functions and classes.
"""

"""
9.1. Putting a wrapper around a function

Problem: you want to put a wrapper layer around that adds extra processing (eg: logging, timing etc)

Solution: decorator function
"""

import time
from functools import wraps

def timethis(func):
    """
    decorator that reports the execution time.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(func.__name__, end-start)
        return result
    return wrapper

@timethis
def countdown(n):
    """
    counts down
    """
    while n > 0:
        n -= 1

countdown(1000000)
countdown(100000000)

"""
A decorator is a function that accepts a function as input and returns a new function
as output, whenever we write code like this:

    @timethis
    def countdown(n):
        ....
        ....

it is same as if you had performed these separate steps:

    countdown = timethis(countdown)
"""

"""
Aa an aside, built-in decorators such as @staticmethod, @classmethod and @property
works in the same way.

    class A:
        @classmethod
        def method(cls):
            pass

is equivalent to
    method = classmethod(method)
"""
