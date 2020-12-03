"""
9.19. Initializing class members at definition time

Problem: You want to initialize parts of a class definition once at the time a class
         is defined, not when instances are created.

Solution: Performing initialization or setup actions at the time of class definition is
          a classic use of metaclasses. Essentially, a metaclass is triggered at the point
          of a definition, at which point you can perform additional steps.
"""

import operator
import typing

class StructTupleMeta(type):
    def __init__(cls, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for n, name in enumerate(cls._fields):
            setattr(cls, name, property(operator.itemgetter(n)))

class StructTuple(tuple, metaclass=StructTupleMeta):
    _fields = []
    def __new__(cls, *args):
        if len(args) != len(cls._fields):
            raise ValueError(f"{len(cls._fields)} arguments required..")
        return super().__new__(cls, args)

class Stock(StructTuple):
    _fields = ['name', 'shares', 'price']

class Point(StructTuple):
    _fields = ['x', 'y']

s = Stock("ACME", 50, 91.1)
print(s)
print('- ' * 50)
# ==================================================================================

"""
9.20. Implementing Multiple Dispatch with Function Annotations

Problem: You've learned function argument annotations and you have a thought that you
         might be able to use them to implement multiple-dispatch (method overloading)
         based on types. However, you're not quite sure what's involved (or if it's even a good idea)

Solution: This recipe is based on a simple observation -- namely, that since Python allows
          arguments to be annotated, perhaps it might be possible to write code like this:
"""
class Spam:
    def bar(self, x: int, y: int):
        print("Bar 1: ", x, y)
    def bar(self, s: str, n: int=0):
        print("Bar 2: ", s, n)

s = Spam()
s.bar(2, 3)    # prints Bar 1: 2 3
s.bar("Hello") # prints Bar 2: hello 0

# Here is the start of a solution that does just that, using a combination of metclass
# and descriptors

import inspect
import types

class MultiMethod:
    """
    Represents a single multimethod
    """
    def __init__(self, name) -> None:
        self._methods = {}
        self.__name__ = name

    def register(self, meth):
        """
        Register a new method as a multimethod
        """
        sig = inspect.signature(meth)
        # build a type signature from the method's annotations
        types = []
        for name, parm in sig.parameters.items():
            if name == "self":
                continue
            if parm.annotation is inspect.Parameter.empty:
                raise TypeError(
                    f"Argument {name} must be annotated with a type"
                )
            if not isinstance(parm.annotation, type):
                raise TypeError(
                    f"Argument {name} annotation must be a type"
                )
            if parm.default is not inspect.Parameter.empty:
                self._methods[tuple(types)] = meth
            types.append(parm.annotation)

        self._methods[tuple(types)] = meth

    def __call__(self, *args):
        """
        Call a method based on type signature of the arguments
        """
        types = tuple(type(arg) for arg in args[1:])
        meth = self._methods.get(types, None)
        if meth:
            return meth(*args)
        else:
            raise TypeError(f"No matching method for types {types}")

    def __get__(self, instance, cls):
        """
        Descriptor method needed to make calls work in a class
        """
        if instance is not None:
            return types.MethodType(self, instance)
        else:
            return self

class MultiDict(dict):
    """
    Special dictionary to build multimethods in a metaclass
    """
    def __setitem__(self, key, value) -> None:
        if key in self:
        # if key already exists, it must be a multimethod or callable
            current_value = self[key]
            if isinstance(current_value, MultiMethod):
                current_value.register(value)
            else:
                mvalue = MultiMethod(key)
                mvalue.register(current_value)
                mvalue.register(value)
                super().__setitem__(key, mvalue)
        else:
            super().__setitem__(key, value)

class MultipleMeta(type):
    """
    Metaclass that allows multiple dispatch of methods
    """
    def __new__(cls, clsname, bases, clsdict):
        return type.__new__(cls, clsname, bases, dict(clsdict))

    @classmethod
    def __prepare__(cls, clsname, bases):
        return MultiDict()

# To use this class, you write code like this:
class Spam(metaclass=MultipleMeta):
    def bar(self, x:int, y:int):
        print(f"Bar 1: {x}, {y}")
    def bar(self, s:str, n:int=0):
        print(f"Bar 2: {s}, {n}")

# Example: overloaded __init__
import time

class Date(metaclass=MultipleMeta):
    def __init__(self, year:int, month:int, day:int) -> None:
        self.year = year
        self.month = month
        self.day = day

    def __init__(self) -> None:
        t = time.localtime()
        self.__init__(t.tm_year, t.tm_mon, t.tm_mday)

s = Spam()
s.bar(2, 3)
s.bar('Hello')
s.bar('Hello', 5)
print('-' * 50)
# ======================================================

import types

class multimethod:
    def __init__(self, func) -> None:
        self._methods = {}
        self.__name__ = func.__name__
        self._default = func

    def match(self, *types):
        def register(func):
            ndefaults = len(func.__defaults__) if func.__defaults__ else 0
            for n in range(ndefaults+1):
                self._methods[types[:len(types) - n]] = func
            return self
        return register

    def __call__(self, *args):
        types = tuple(type(arg) for arg in args[1:])
        meth = self._methods.get(types, None)
        if meth:
            return meth(*args)
        else:
            return self._default(*args)

    def __get__(self, instance, cls):
        if instance is not None:
            return types.MethodType(self, instance)
        else:
            return self

class Spam:
    @multimethod
    def bar(self, *args):
        #default method called if no match
        raise TypeError("No matching method for bar")

    @bar.match(int, int)
    def bar(self, x, y):
        print(f"Bar 1: {x}, {y}")

    @bar.match(str, int)
    def bar(self, s, n=0):
        print(f"Bar 2: {s}, {n}")
