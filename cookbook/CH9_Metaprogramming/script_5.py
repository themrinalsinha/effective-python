"""
9.6. Defining a decorator that takes an optional argument

Problem: You would like to write s single decorator that can be used without arguments,
         such as @decorator, or with optional arguments, @decorator(x, y, z). However,
         there seems to be no straightforward way to do it due to differences in calling
         conventions between simple decorator and decorators taking arguments.
"""

from functools import wraps, partial
import logging

def logged(func=None, *, level=logging.DEBUG, name=None, message=None):
    if func is None:
        return partial(logged, level=level, name=name, message=message)

    logname = name if name else func.__module__
    log     = logging.getLogger(logname)
    logmsg  = message if message else func.__name__

    @wraps(func)
    def wrapper(*args, **kwargs):
        log.log(level, logmsg)
        return func(*args, **kwargs)
    return wrapper

# example use
@logged
def add(x, y):
    return x + y

@logged(level=logging.CRITICAL, name="example")
def spam():
    print("Spam!")
print(f"{'-'*50}")
print()
# =======================================================================================

"""
9.7. Enforcing Type Checking on a function using a decorator

Problem: You want to optionally enforce type checking of function arguments as a kind
         of assertion or contract.
"""

from inspect import signature
from functools import wraps

def typeassert(*ty_args, **ty_kwargs):
    def decorate(func):
        # if in optimized mode, disable type checking.
        if not __debug__:
            return func

        # map function argument names to supplied types
        sig = signature(func)
        bound_types = sig.bind_partial(*ty_args, **ty_kwargs).arguments

        @wraps(func)
        def wrapper(*args, **kwargs):
            bound_values = sig.bind(*args, **kwargs)
            # enforce type assertion across supplied arguments
            for name, value in bound_values.arguments.items():
                if name in bound_types:
                    if not isinstance(value, bound_types[name]):
                        raise TypeError(f"Argument {name} must be {bound_types[name]}")

            return func(*args, **kwargs)
        return wrapper
    return decorate

# You'll find that this decorator is rather flexible, allowing types to be specified for
# all or a subset of a function's arguments. Moreover, types can be specified by position
# or by keyword.
@typeassert(int, z=int)
def spam(x, y, z=42):
    print(x, y, z)

spam(1, 2, 3)
spam(1, "Hello", 3)
# spam(1, "h", "w") # will throw error
