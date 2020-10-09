"""
8.11. Simplifying the initialization of data structures

Problem: You're writing a lot of classes that serve as data structures, but you are getting
         tired of writing highly repetitive and boilerplate __init__() functions.

Solutions: You can often generalized the initialization of data structures into a single
           __init__() function defined in a common base class.
"""

class Structure:
    _fields = [] # class variable that specifies expected fields
    def __init__(self, *args) -> None:
        if len(args) != len(self._fields):
            raise TypeError(f"Expected {len(self._fields)} arguments")

        # set the arguments
        for name, value in zip(self._fields, args):
            setattr(self, name, value)

# example class definition
class Stock(Structure):
    _fields = ['name', 'shares', 'price']

class Point(Structure):
    _fields = ['x', 'y']

class Circle(Structure):
    _fields = ['radius']

    def area(self):
        return 3.14 * self.radius ** 2

s1 = Stock('ACME', 50, 91.1)
# s2 = Stock('ACME', 50) # this will throw TypeError


"""
Should you decide to support keyword arguments, there are several design options.
One choice is to map the keyword argument so that they only correspond to the
attribute name specified in _fields
"""
class Structure:
    _fields = []
    def __init__(self, *args, **kwargs) -> None:
        if len(args) > len(self._fields):
            raise TypeError(f"Expected {len(self._fields)} arguments.")

        # set all the positional arguments
        for name, value in zip(self._fields, args):
            setattr(self, name, value)

        # set the remaining keyword arguments
        for name in self._fields[len(args):]:
            setattr(self, name, kwargs.pop(name))

        # check for the remaining unknown arguments
        if kwargs:
            raise TypeError(f"Invalid  argument(s): {','.join(kwargs)}")


class Stock(Structure):
    _fields = ['name', 'shares', 'price']

s1 = Stock('ACME', 50, 90.01)
s2 = Stock('ACME', 50, price=91.1)
print(s1, s2)



"""
Another possible choice is to use keyword arguments as a means for adding additional
attributes to the structure not specified in _fields
"""
class Structure:
    _fields = []
    def __init__(self, *args, **kwargs) -> None:
        if len(args) > len(self._fields):
            raise TypeError(f"Expected {len(self._fields)} arguments.")

        # set all the positional arguments
        for name, value in zip(self._fields, args):
            setattr(self, name, value)

        # set the additional arguments (if any)
        extra_args = kwargs.keys() - self._fields
        for name in extra_args:
            setattr(self, name, kwargs.pop(name))
        if kwargs:
            raise TypeError(f"Duplicate values for {','.join(kwargs)}")

class Stock(Structure):
    _fields = ['name', 'shares', 'price']

s1 = Stock('ACME', 50, 91.1)
s2 = Stock('ACME', 50, 91.1, date='8/2/2012')
print(s1, s2)

"""
This technique for defining a general purpose __init__() method can be extremely useful
if you're ever writing a program built around a large number of small data structures.

One subtle aspect of the implementation concerns the mechanism used to set value
using the setattr() function. Instead of doing that, you might be inclined to directly
access the instance dictionary.
"""
class Structure:
    # class variable that specifies expected fields
    _fields = []
    def __init__(self, *args) -> None:
        if len(args) != len(self._fields):
            raise TypeError(f"Expected {len(self._fields)} arguments")

        # set the arguments (alternate)
        self.__dict__.update(zip(self._fields, args))
