"""
9.21. Avoiding Repetitive Property Methods

Problem: You are writing classes where you are repeatedly having to define property
         methods that perform common tasks, such as type checking. You would like to
         simplify the code so there is not so much code repetition.
"""

class Person:
    def __init__(self, name, age) -> None:
        self.name = name
        self.age = age

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("name must be a string")
        self._name = value

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if not isinstance(value, int):
            raise TypeError("Age must be an int")
        self._age = value


# As you ca see, a lot of code is being written simply to enforce some type assertion
# on attribute values. Whenever you see code like this, you should explore different
# way of simplifying it. One possible approach is to make a function that simply defines
# the property for you and returns it.
def typed_property(name, expected_type):
    storage_name = '_' + name

    @property
    def prop(self):
        return getattr(self, storage_name)

    @prop.setter
    def prop(self, value):
        if not isinstance(value, expected_type):
            raise TypeError(f"{name} must be a {expected_type}")
        setattr(self, storage_name, value)
    return prop

class Person:
    name = typed_property('name', str)
    age = typed_property('age', int)
    def __init__(self, name, age) -> None:
        self.name = name
        self.age = age

# ===================================================================================
from functools import partial

String = partial(typed_property, expected_type=str)
Integer = partial(typed_property, expected_type=int)

class Person:
    name = String("name")
    age = Integer("age")
    def __init__(self, name, age) -> None:
        self.name = name
        self.age = age
print('-' * 50)
# ===================================================================================

"""
9.22. Defining context managers the easy way.

Problem: You want to implement new kinds of context managers for use with the 'with' statement

Solution: Once of the most straightforward ways to write a new context manager is to use
          the @contextmanager decorator in the contextlib module. Here is an example of
          a context manager that times the execution of a code block.
"""
import time
from contextlib import contextmanager

@contextmanager
def timethis(label):
    start = time.time()
    try:
        yield
    finally:
        end = time.time()
        print(f"{label}: {end-start}")

with timethis("counting"):
    n = 1000000
    while n > 0:
        n -= 1

# in this timethis() function, all of the code prior to the yield executes as the __enter__()
# method of a context manager. All of the code after the yield executes as the __exit__()
# method. If there was an exception. it is raised at the yield statement.

@contextmanager
def list_transaction(orig_list):
    working = list(orig_list)
    yield working
    orig_list[:] = working

items = [1, 2, 3]
with list_transaction(items) as working:
    working.append(4)
    working.append(5)
