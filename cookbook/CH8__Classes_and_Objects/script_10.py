"""
8.13. Implementing a Data Model or Type System

Problem: You want to define various kinds of data structures, but want to enforce constraints
         on the values that are allowed to be assigned to certain attributes.

Solution: In this problem, you are basically faced with the task of placing checks or assertions on
the setting of certain instance attributes. To do this, you need to customize the setting
of attributes on a per-attribute basis. To do this, you should use descriptors.
"""

# Base class. Uses a descriptor to set a value
from os import name


class Descriptor:
    def __init__(self, name=None, **opts) -> None:
        self.name = name
        for key, value in opts.items():
            setattr(self, key, value)

    def __set__(self, instance, value):
        print(f"INSTANCE: {instance}")
        print(f"INSTANCE (dict): {instance.__dict__}")
        print(f"VALUE: {value}")
        instance.__dict__[self.name] = value

# Descriptor for enforcing types
class Typed(Descriptor):
    expected_type = type(None)

    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError('Expected ', str(self.expected_type))
        super().__set__(instance, value)

# Descriptor for enforcing values
class Unsigned(Descriptor):
    def __set__(self, instance, value):
        if value < 0:
            raise ValueError("Expected >= 0")
        super().__set__(instance, value)

class MaxSized(Descriptor):
    def __init__(self, name=None, **opts) -> None:
        if 'size' not in opts:
            raise TypeError("Missing size option")
        super().__init__(name, **opts)

    def __set__(self, instance, value):
        if len(value) >= self.size:
            raise ValueError(f"Size must be < {str(self.size)}")
        super().__set__(instance, value)

"""
These classes should be viewed as basic building blocks from which you construct a data
model or type system. Continuing, here is some code that implements some different kinds
of data
"""
class Integer(Typed):
    expected_type = int

class UnsignedInteger(Integer, Unsigned):
    pass

class Float(Typed):
    expected_type = float

class UnsignedFloat(Float, Unsigned):
    pass

class String(Typed):
    expected_type = str

class SizedString(String, MaxSized):
    pass

# Using these type objects, it is now possible to define a class such as this:
class Stock:
    name = SizedString('name', size=8)
    shares = UnsignedInteger('shares')
    price = UnsignedFloat('price')

    def __init__(self, name, shares, price) -> None:
        self.name = name
        self.shares = shares
        self.price = price

s = Stock('ACME', 50, 91.1)
print(s.name)
print(s.shares)
s.shares = 100
print(s.shares)
# s.shares = -10 # ValueError: Expected >= 0


"""
There are some techniques that can be used to simplify the specification of constraints in class.
One approach is to use a class decorator
"""
# class decorator to apply constraints
def check_attributes(**kwargs):
    def decorate(cls):
        for key, value in kwargs.items():
            if isinstance(value, Descriptor):
                value.name = key
                setattr(cls, key, value)
            else:
                setattr(cls, key, value(key))
        return cls
    return decorate

@check_attributes(name=SizedString(size=8),
                  shares=UnsignedInteger,
                  price=UnsignedFloat)
class Stock:
    def __init__(self, name, shares, price) -> None:
        self.name = name
        self.shares = shares
        self.price = price

# another approach to simplify the specification of constraints is to use a metclass.
# Example:
# A metaclass that applies checking
class checkedmeta(type):
    def __new__(cls, clsname, bases, methods):
        # attach attribute names to the descriptors
        print(f"CLS: {cls}")
        print(f"classname: {clsname}")
        print(f"bases: {bases}")
        print(f"methods: {methods}")

        for key, value in methods.items():
            if isinstance(value, Descriptor):
                value.name = key
        return type.__new__(cls, clsname, bases, methods)

# example
class Stock(metaclass=checkedmeta):
    name = SizedString(size=8)
    shares = UnsignedInteger()
    price = UnsignedFloat()

    def __init__(self, name, shares, price) -> None:
        self.name = name
        self.shares = shares
        self.price = price

"""
This recipe involves a number of advanced techniques, including descriptors, mixin classes,
the use of super(), class decorators, and metaclasses.
"""
