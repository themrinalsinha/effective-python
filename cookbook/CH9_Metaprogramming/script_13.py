"""
9.17. Enforcing Coding Conventions in Classes

Problem: Your program consists of a large class hierarchy and you would like to enforce
         certain kinds of coding conventions (or perform diagnostics) to help maintain
         programmer sanity.

Solution: If you want to monitor the definition of classes, you can often do it by defining
          a metaclass. A basic metaclass is usually defined by inheritance from type and
          redefining its __new__() method or __init__() method.
"""

class MyMeta(type):
    def __new__(self, clsname, bases, clsdict):
        # clsname is name of class being defined
        # bases is tuple of base classes
        # clsdict is class dictionary
        return super().__new__(cls, clsname, bases, clsdict)

# alternatively, if __init__() is defined
class MyMeta(type):
    def __init__(self, clsname, bases, clsdict) -> None:
        # clsname is name of class being defined
        # bases is tuple of base classes
        # clsdict is class dictionary
        super().__init__(clsname, bases, clsdict)

# To use a metaclass, you would generally incorporate it into a top-level base class
# from which other objects inherit.
class Root(metaclass=MyMeta):
    pass

class A(Root):
    pass

class B(Root):
    pass

# A key feature of metaclass is that it allows you to examine the content of a class at
# the time of definition. Inside the redefined __init__() method, you are free to inspect
# the class dictionary, base classes, and more. Moreover, once a metaclass has been specified
# for a class, it gets inherited by all of the subclasses. Thus, a sneaky framework builder
# can specify a metaclass for one of the top-level classes in a large hierachical and capture
# the definition of all classes under it.

class NoMixinCaseMeta(type):
    def __new__(cls, clsname, bases, clsdict):
        for name in clsdict:
            if name.lower() != name:
                raise TypeError("Bad attribute name: " + name)
        return super().__new__(cls, clsname, bases, clsdict)

class Root(metaclass=NoMixinCaseMeta):
    pass

class A(Root):
    def foo_bar(self):
        pass

# class B(Root):
#     def fooBar(self): # will throw TypeError
#         pass

# As a more advanced and useful example, here is a metaclass that checks the definition
# or redefined methods to make sure they have the same calling signature as the original
# method in the superclass.
from inspect import signature
import logging

class MatchSignaturesMeta(type):
    def __init__(self, clsname, bases, clsdict) -> None:
        super().__init__(clsname, bases, clsdict)

        sup = super(self, self)
        for name, value in clsdict.items():
            if name.startswith("_") or not callable(value):
                continue

            # get the previous definition (if any) and compare the signatures
            prev_dfn = getattr(sup, name, None)
            if prev_dfn:
                prev_sig = signature(prev_dfn)
                val_sig = signature(value)
                if prev_sig != val_sig:
                    logging.warning("Signature mismatch in %s. %s != %s", value.__qualname__, prev_sig, val_sig)


# example
class Root(metaclass=MatchSignaturesMeta):
    pass

class A(Root):
    def foo(self, x, y):
        pass

    def spam(self, x, *, z):
        pass

# class with redefined methods, but slightly different signatures
class B(A):
    def foo(self, a, b):
        pass

    def spam(self, x, z):
        pass
