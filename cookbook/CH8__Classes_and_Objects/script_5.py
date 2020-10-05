"""
8.8. Extending a property in a subclass

Problem: within a subclass, you want to extend the functionality of a property defined
         in a parent class.
"""

class Person:
    def __init__(self, name) -> None:
        self.name = name

    # getter function
    @property
    def name(self):
        return self._name

    # setter function
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Expected a string")
        self._name = value

    # deleter function
    @name.deleter
    def name(self):
        raise AttributeError("Can't delete attribute")

# Here is an example of a class that inherits from Person and extends the
# name property with new functionality.
class SubPerson(Person):
    @property
    def name(self):
        print("Getting name")
        return super().name

    @name.setter
    def name(self, value):
        print(f"Setting name to: {value}")
        super(SubPerson, SubPerson).name.__set__(self, value)

    @name.deleter
    def name(self):
        print("Deleting name")
        super(SubPerson, SubPerson).name.__delete__(self)

s = SubPerson("Guido")
print(f"NAME: {s.name}")
s.name = 'Larry'

# If you only want to extend one of the methods of a property,
# use code such as the following:
class SubPerson(Person):
    @Person.name.getter
    def name(self):
        print(f"Getting name")
        return super().name

# or, alternatively, for just the setter, use the code:
class SubPerson(Person):
    @Person.name.setter
    def name(self, value):
        print(f"Setting name to: {value}")
        super(SubPerson, SubPerson).name.__set__(self, value)
