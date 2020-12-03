"""
9.18. Defining classes programmatically

Problem: You're writing code that ultimately needs to create a new class object. You've
         thought about emitting emit class source code to a string and using a function
         such as exec() to evaluate it, but you'd prefer a more elegant solution.

Solution: You can use the function types.new_class() to instantiate new class objects. all
          you need to de is provide the name of the class, tuple of parents classes, keyword
          arguments, and a callback that populates the class dictionary with members.
"""

def __init__(self, name, shares, price):
    self.name = name
    self.shares = shares
    self.price = price

def cost(self):
    return self.shares * self.price

cls_dict = {
    '__init__': __init__,
    'cost': cost,
}

import types
Stock = types.new_class("Stock", (), {}, lambda ns: ns.update(cls_dict))
Stock.__module__ = __name__

print(Stock) # it will work like a normal class.
# ========================================================================

import abc
Stock = types.new_class("Stock", (), {"metaclass": abc.ABCMeta}, lambda ns: ns.update(cls_dict))
Stock.__module__ = __name__
print(Stock)

# Being able to manifacture new class objects can be useful in certain contexts. One of
# the more familiar examples involves the collections.namedtuple() function.
from collections import namedtuple

Stock = namedtuple("Stock", ["name", "shares", "price"])
print(Stock)

# namedtuple() uses exec() instead of the technique shown here. However, here is a simple
# variant that creates a class directly
import operator
import types
import sys

def named_typle(classname, fieldnames):
    # populate a dictionary of field property accessors
    cls_dict = { name: property(operator.itemgetter(n)) for n, name in enumerate(fieldnames) }

    # make a __new__ function and add to the class dict
    def __new__(cls, *args):
        if len(args) != len(fieldnames):
            raise TypeError("Expected {} arguments".format(len(fieldnames)))
        return tuple.__new__(cls, args)

    cls_dict['__new__'] = __new__

    # make the class
    cls = types.new_class(classname, (tuple,), {}, lambda ns: ns.update(cls_dict))

    # set the module to that of the caller
    cls.__module__ = sys._getframe(1).f_globals['__name__']
    return cls

Point = named_typle("Point", ["x", "y"])
print(Point)
