"""
9.2. Preserving function metadata when writing decorators

Problem: you've written a decorator, but when you apply it to a function, important
         metadata such as the name, doc string, annotation and calling signature are lost.
"""
import time
from functools import wraps

def timethis(func):
    """
    Decorator that reports the execution time.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(func.__name__, end-start)
        return result
    return wrapper

# Here is an example of using the decorator and examining the result function metadata:
@timethis
def countdown(n: int):
    """
    Counts down
    """
    while n > 0:
        n -= 1

countdown(1000000)
print(countdown.__name__)
print(countdown.__doc__)
print(countdown.__annotations__)

# NOTE: Copyting decorator metadata is an important part of writing decorators. If you
#       forget to use @wraps you'll find the decorator function loses all sorts of useful information.
print('- ' * 50)
# ====================================================================================

"""
9.3 Unwrapping a decorator

Problem: A decorator has been applied to a function, but you want to "undo" it, gaining access
         to the original unwrapped function.
"""

@timethis
def add(x, y):
    return x + y

original_function = add.__wrapped__
print(original_function(5, 6))

# Gaining direct access to the unwrapped function behind a decorator can be useful for
# debugging, introspection, and other operations involving functions. However, this
# recipe only works if the implementation of a decorator properly copies metadata using
# @wraps from the functools module or sets the __wrapped__ attribute directly.
