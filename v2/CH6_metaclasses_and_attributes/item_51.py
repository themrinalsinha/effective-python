"""
Item 51: Prefer class decorators over metaclasses for composable class extensions


Although metaclasses allow you to customize class creation in multiple ways, they
still fall short of handling every situation that may arise.

Ex: say that i want to decorate all the method of a class with a helper that prints
arguments, return values, and exceptions raised. here i define the debugging decorator.
"""

from functools import wraps

def trace_func(func):
    if hasattr(func, 'tracing'): # only decorate once
        return func

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = None
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            result = e
            raise
        finally:
            print(f'{func.__name__}({args!r}, {kwargs!r}) -> {result!r}')

    wrapper.tracing = True
    return wrapper


# I can apply this decorator to various special methods in my new dict subclass.
class TraceDict(dict):
    @trace_func
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @trace_func
    def __setitem__(self, *args, **kwargs):
        return super().__setitem__(*args, **kwargs)

    @trace_func
    def __getitem__(self, *args, **kwargs):
        return super().__getitem__(*args, **kwargs)

# And i can verify that these methods are decorated by interacting with an
# instance of the class:
trace_func = TraceDict([('hi', 1)])
trace_func['there'] = 2
trace_func['hi']

# The problem with this code is that I had to redefine all of the methods that I wanted
# to decorate with @trace_func. This is redundant boilerplate that's hard to read and
# error prone. Further, if a new method is later added to the dict superclass, it won't
# be decorated unless i also define it in TraceDict.
# ========================================================================================

"""
one way to solve this problem is to use a metaclass to automatically decorate all
methods of a class. here, i implement this behavior by wrapping each function or
method in the new type with the trace_func decorator
"""

import types

trace_types = (
    types.MethodType,
    types.FunctionType,
    types.BuiltinFunctionType,
    types.BuiltinMethodType,
    types.MethodDescriptorType,
    types.ClassMethodDescriptorType
)

class TraceMeta(type):
    def __new__(meta, name, bases, class_dict):
        klass = super().__new__(meta, name, bases, class_dict)

        for key in dir(klass):
            value = getattr(klass, key)
            if isinstance(value, trace_types):
                wrapped = trace_func(value)
                setattr(klass, key, wrapped)

        return klass

# Now, I can declare my dict subclass by using the Tracemeta metaclass and verify
# that it works as expected:
# class TraceDict(dict, metaclass=TraceMeta):
#     pass

# trace_dict = TraceDict([('hi', 1)])
# trace_dict['there'] = 2
# trace_dict['hi']

# # try:
# #     trace_dict['does not exist']
# # except KeyError:
# #     pass # expected

"""
Things to Remember

✦ A class decorator is a simple function that receives a class instance
  as a parameter and returns either a new class or a modified version
  of the original class.

✦ Class decorators are useful when you want to modify every method
  or attribute of a class with minimal boilerplate.

✦ Metaclasses can’t be composed together easily, while many class
  decorators can be used to extend the same class without conflicts.
"""
