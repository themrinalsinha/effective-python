"""
9.10. Applying decorators to class and static methods

Problem: You want to apply a decorator to a class or static method.

Solution: applying decorators to class and static method is straightforward, but make sure
          that your decorator are applied before @classmethod or @staticmethod
"""
import time
from functools import wraps

# a simple decorator
def timethis(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        r = func(*args, **kwargs)
        end = time.time()
        print(end-start)
        return r
    return wrapper

# class illustrating application of the decorator to different kinds of methods
class Spam:
    @timethis
    def instance_method(self, n):
        print(self, n)
        while n > 0:
            n -= 1

    @classmethod
    @timethis
    def class_method(cls, n):
        print(cls, n)
        while n > 0:
            n -= 1

    @staticmethod
    @timethis
    def static_method(n):
        print(n)
        while n > 0:
            n -= 1

# The resulting class and static method should operate normally, but have the extra
# timing:
s = Spam()
s.instance_method(1000000)
Spam.class_method(1000000)
Spam.static_method(1000000)
print('-' * 50)
# ===================================================================================

"""
9.11. Writing decorators that add arguments to wrapped functions

Problem: you want to write a decorator that adds an extra argument to the calling signature
         of the wrapped function. However, the added argument can't interfere with the existing
         calling conventions of the function.

Solution: Extra arguments can be injected into the calling signature using keyword-only
          arguments.
"""
from functools import wraps

def optional_debug(func):
    @wraps(func)
    def wrapper(*args, debug=False, **kwargs):
        if debug:
            print(f"Calling: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@optional_debug
def spam(a, b, c):
    print(a, b, c)

spam(1, 2, 3)
spam(1, 2, 3, debug=True)
print('-' * 50)
# ===================================================================================
