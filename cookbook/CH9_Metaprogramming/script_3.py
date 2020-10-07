"""
9.4. Defining a decorator that takes arguments

Problem: you want to write a decorator function that takes arguments
"""
import logging
from functools import wraps

def logged(level, name=None, message=None):
    """
    Add logging to a function.
    @level   - is a logging level
    @name    - is the logger name, and message.
    @message - is the log message
    """

    def decorator(func):
        logname = name if name else func.__module__
        logmsg = message if message else func.__name__
        log = logging.getLogger(logname)

        @wraps(func)
        def wrapper(*args, **kwargs):
            log.log(level, logmsg)
            return func(*args, **kwargs)
        return wrapper
    return decorator


# example use
@logged(logging.DEBUG)
def add(x, y):
    return x + y

@logged(logging.CRITICAL, 'example')
def spam():
    print("SPAM!")

add(12, 24)

"""
Writing a decorator that takes arguments is tricky because of the underlying calling
sequence involved. Specially, if you have code like this:

    @decorator(x, y, z)
    def func(a, b):
        pass

The decoration process evaluates as follows:
    def func(a, b):
        pass

    func = decorator(x,y,z)(func)
"""
