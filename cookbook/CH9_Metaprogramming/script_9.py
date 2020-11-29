"""
9.13. Using a Metaclass to Control Instance Creation

Problem: You want to change the way in which instances are created in order to implement
         singletons, caching, or other similar features.
"""

from typing import Any

# as python programmer know, if you define a class, you call it like a function to
# create instance, Eg:
class Spam:
    def __init__(self, name) -> None:
        self.name = name

a = Spam("Guido")
b = Spam("Diana")

# If you want to customize this step, you can do it by defining a metaclass and
# reimplementing its __call__() method in some way.

class NoInstance(type):
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        raise TypeError("Can't instantiate directly")

# Example
class Spam(metaclass=NoInstance):
    @staticmethod
    def grok(x):
        print("Spam.grok")

# In this case, users can call the defined static method, but it's impossible to create
# an instance in the normal way. Eg:
Spam.grok(42)
# s = Spam() # will throw error

# Now, suppose you want to implement the singleton pattern (i.e., a class where only on
# instance is ever created). That is also relatively straightforward, as shown here..
class Singleton(type):
    def __init__(self, *args, **kwargs) -> None:
        self.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        if self.__instance is None:
            self.__instance = super().__call__(*args, **kwargs)
            return self.__instance
        else:
            return self.__instance

# Example
class Spam(metaclass=Singleton):
    def __init__(self) -> None:
        print("Creating Spam...")

a = Spam()
b = Spam()
print(a is b)

# finally, suppose you want to create cached instances, here's a metaclass to implement it.
import weakref

class Cached(type):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__cache = weakref.WeakValueDictionary()

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        if args in self.__cache:
            return self.__cache[args]
        else:
            obj = super().__call__(*args)
            self.__cache[args] = obj
            return obj

# Example
class Spam(metaclass=Cached):
    def __init__(self, name) -> None:
        print("Creating Spam({!r})".format(name))
        self.name = name

a = Spam("Guido")
b = Spam("Diana")
c = Spam("Guido") # cached

print(a is b)
print(b is c)
print(c is a) # cached value returned
