"""
9.5. Defining a decorator with User Adjustable Attributes

Problem: You want to write a decorator function that wraps a function, but has user
         adjustable attributes that can be used to control the behavior of the decorator at
         runtime.
"""

from functools import wraps, partial
import logging

# utility decorator to attach a function as an attribute of obj
def attach_wrapper(obj, func=None):
    if func is None:
        return partial(attach_wrapper, obj)
    setattr(obj, func.__name__, func)
    return func

def logged(level, name=None, message=None):
    """
    Add logging to a function. level is the logging level, name is logger name & message
    is the log message. If name and message aren't specified they default to the function's
    module and name.
    """
    def decorate(func):
        logname = name if name else func.__module__
        log = logging.getLogger(logname)
        logmsg = message if message else func.__name__

        @wraps(func)
        def wrapper(*args, **kwargs):
            log.log(level, logmsg)
            return func(*args, **kwargs)

        # attach setter functions
        @attach_wrapper(wrapper)
        def set_level(newlevel):
            nonlocal level
            level = newlevel

        @attach_wrapper(wrapper)
        def set_message(newmsg):
            nonlocal logmsg
            logmsg = newmsg

        return wrapper
    return decorate

# example use
@logged(logging.DEBUG)
def add(x, y):
    return x + y

@logged(logging.CRITICAL, 'example')
def spam():
    print("Spam!")

# Here is an interactive session that shows the various attributes being changed after definition.
logging.basicConfig(level=logging.DEBUG)
print(add(2, 3))

# change the log message
add.set_message("Add called")
print(add(2, 3))

# change the log level
add.set_level(logging.WARNING)
print(add(2, 3))
