"""
9.13. Capturing class attribute definition order

Problem: you want to automatically record the order in which attributes and methods are
         defined inside a class body so that you can use it in various operations...
         eg: serializing, mapping to database etc.

Solution: Capturing information about the body of class definition is easily accomplished
          through the use of metaclass. Here is an example of a metaclass that uses an
          OrderedDict to capture order of descriptors.
"""
from typing import Any
from collections import OrderedDict


# a set of descriptors for various types
class Typed:
    _expected_type = type(None)
    def __init__(self, name=None) -> None:
        self._name = name

    def __set__(self, instance, value):
        if not isinstance(value, self._expected_type):
            raise TypeError("Expected " + str(self._expected_type))
        instance.__dict__[self._name] = value

class Integer(Typed):
    _expected_type = int

class Float(Typed):
    _expected_type = float

class String(Typed):
    _expected_type = str


# metaclass that uses an OrderedDict for class body
class OrderedMeta(type):
    def __new__(cls, cls_name, bases, cls_dict) -> Any:
        d = dict(cls_dict)
        order = []
        for name, value in cls_dict.items():
            if isinstance(value, Typed):
                value._name = name
                order.append(name)

        d['_order'] = order
        return type.__new__(cls, cls_name, bases, d)

    @classmethod
    def __prepare__(cls, cls_name, bases):
        return OrderedDict()

# In this metaclass, the definition order of descriptors is captured by using an
# OrderedDict during the execution of the class body. The resulting order of names
# is then extracted from the dictionary and stored into a class attribute _order.
# This can then be used by methods of the class in various ways. Ex: here is a
# simple class that uses the ordering to implement a method for serializing the instance
# data as a line of CSV data.

class Structure(metaclass=OrderedMeta):
    def as_csv(self):
        return ','.join(str(getattr(self, name)) for name in self._order)

# Example
class Stock(Structure):
    name = String()
    shares = Integer()
    price = Float()

    def __init__(self, name, shares, price) -> None:
        self.name = name
        self.shares = shares
        self.price = price

# Here is an interactive session illustrating the use of Stock class in the example:
s = Stock("GOOG", 100, 490.1)
print(s)
print(s.name)
print(s.shares)
print(s.price)
print('- ' * 50)
# ----------------------------------------------------------------------------------

from collections import OrderedDict

class NoDupOrderedDict(OrderedDict):
    def __init__(self, clsname) -> None:
        self.clsname = clsname
        super().__init__()

    def __setitem__(self, name, value) -> None:
        if name in self:
            raise TypeError(f"{name} already defined in {self.clsname}")
        super().__setattr__(name, value)

class OrderedMeta(type):
    def __new__(cls, clsname, bases, clsdict) -> Any:
        d = dict(clsdict)
        d['_order'] = [name for name in clsdict if name[0] != '_']
        return type.__new__(cls, clsname, bases, d)

    @classmethod
    def __prepare__(cls, clsname, bases):
        return NoDupOrderedDict(clsname)

# here's what happens if you use this metaclass and make a class with duplicate entries
class A(metaclass=OrderedMeta):
    def spam(self):
        pass
    def spam(self):
        pass


