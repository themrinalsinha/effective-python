"""
8.9. Creating a new kind of class or instance attribute

Problem: You want to create an entirely new kind of instance attribute, define its
         functionality in the form of a descriptor class.
"""

# Descriptor attribute for an integer type-checking attribute
class Integer:
    def __init__(self, name) -> None:
        self.name = name

    def __get__(self, instance, cls):
        if instance is None:
            return self
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError("Expected an int")
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]

# A descriptor is a class that implements the three core attribute access operations
# (get, set & delete) in the form of __get__(), __set__(), __delete__() special methods.

class Point:
    x = Integer('x')
    y = Integer('y')

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

# when you do this, all access to the descriptor attributes (eg: x or y) is captured by
# the __get__(), __set__(), __delete__() methods.
p = Point(2, 3)
print(p.x)
print(p.y)
# p.x = 2.3 ## will throw type error (it will only accept int)

# As input, each method of a descriptor receives the instance being manipulated. To carry
# out the requested operation, the underlying instance dictionary (the __dict__ attribute)
# is manipulated as appropriate. The self.name attribute of the descriptor holds the dic‐
# tionary key being used to store the actual data in the instance dictionary.
print('- ' * 50)

# IMPORTANT:
# By defining a descriptor, you can capture the core instance operations (get, set, delete)
# at a very low level and completely customize what they do. This gives you great power,
# and is one of the most important tools employed by the writers of advanced libraries
# and frameworks.

# One confusion with descriptors is that they can only be defined at the class level, not
# on a per-instance basis. Thus, code like this will not work:

# Descriptor attribute for an integer type-checked attribute
class Integer:
    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.name]
# NOTE: The reason __get__() looks somewhat complicated is to account for the distinction
# between instance variables and class variables. If a descriptor is accessed as a class vari‐
# able, the instance argument is set to None . In this case, it is standard practice to simply
# return the descriptor instance itself (although any kind of custom processing is also
# allowed).

p = Point(2, 3)
print(p.x) # calls Point.x.__get__(p, Point)
print(Point.x) # calls Point.x.__get__(None, Point)
print()
# ===================================================================================
print(f'{"Advance Descriptor":-^60}')

# Descriptor for a type-checked attribute
class Typed:
    def __init__(self, name, expected_type):
        self.name          = name
        self.expected_type = expected_type

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError("Expected " + str(self.expected_type))
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]

# class decorator that applies it to selection attributes
def typeassert(**kwargs):
    def decorate(cls):
        for name, expected_type in kwargs.items():
            # attach typed descriptor to the class
            setattr(cls, name, Typed(name, expected_type))
        return cls
    return decorate

# Example:
@typeassert(name=str, shares=int, price=float)
class Stock:
    def __init__(self, name, shares, price) -> None:
        self.name   = name
        self.shares = shares
        self.price  = price

x = Stock("APPL", 120, 500.5)
print(x)
# y = Stock("GOOGL", "100", 30.98) # will throw error
