"""
8.4. saving memory when creating a large number of instances

Problem: your program creates a large number (eg. millions) of instances
         and uses a large amount of memory.

Solution: For classes that primarily serve as simple data structures, you can often greatly reduce
the memory footprint of instances by adding the __slots__ attribute to the class defi‐
nition.
"""

class Date:
    __slots__ = ['year', 'month', 'day']
    def __init__(self, year, month, day) -> None:
        self.day   = day
        self.year  = year
        self.month = month

print('- ' * 50)
# ===============================================================================================

"""
8.5. Encapsulating Names in a Class

Problem: you want to encapsulate "private" data on instance of a class, but are
         concerned about python's lack of access control
"""
class A:
    def __init__(self) -> None:
        self._internal = 0  # an internal attribute
        self.public    = 1  # a public attribute

    def public_method(self):
        print("public method")

    def _internal_method(self):
        print("internal method")


class B:
    def __init__(self) -> None:
        self.__private = 0

    def __private_method(self):
        print('Private method called')

    def public_method(self):
        self.__private_method()


class C:
    def __init__(self) -> None:
        super().__init__()
        self.__private = 1 # does not override B.__private

    def __private_method(self):
        print('Private method called')

# Here, the private names __private and __private_method get rename to _c__private
# and _C__private_method, which are different than the mangle names in the base class B.
print('- ' * 50)
# ===============================================================================================

"""
8.6. Creating managed attributes

Problem: You want to add extra processing (eg. type checking or validation) to the
         getting or setting of an instance attribute.
"""

class Person:
    def __init__(self, first_name) -> None:
        self.first_name = first_name

    # getter function
    @property
    def first_name(self):
        return self._first_name

    # setter function
    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str):
            raise TypeError("Expected a string")
        self._first_name = value

    # deleter function (optional)
    @first_name.deleter
    def first_name(self):
        raise AttributeError("Can't delete attribute")

# In the preceding code, there are three related methods, all of which must have the same
# name. The first method is a getter function, and establishes first_name as being a
# property. The other two methods attach optional setter and deleter functions to the
# first_name property. It’s important to stress that the @first_name.setter and
# @first_name.deleter decorators won’t be defined unless first_name was already
# established as a property using @property .

a = Person('Gudio')
print(a.first_name)             # calls the getter
a.first_name = 'Hello there...' # setter (using str)
print(a.first_name)             # calls the getter
