"""
8.25. Creating Cached Instances

Problem: When creating instances of a class, you want to return a cached reference to
         a previous instance created with the same arguments (if any)

Solution: The problem being addressed in this recipe sometimes arises when you want to
          ensure that there is only one instance of a class created for a set of input
          argument.
"""


import logging

# Practical examples include the behavior of libraries, such as the logging module,
# that only want to associate a single logger instance with a given name.
a = logging.getLogger('foo')
b = logging.getLogger('bar')
c = logging.getLogger('foo')

print(a is b)
print(a is c)
print()

# To implement this behavior, you should make use of a factory function that's seperate
# from the class itself. Eg:

class Spam:
    def __init__(self, name) -> None:
        self.name = name

# caching support
import weakref
_spam_cache = weakref.WeakValueDictionary()

def get_spam(name):
    if name not in _spam_cache:
        s = Spam(name)
        _spam_cache[name] = s
    else:
        s = _spam_cache[name]
    return s

a = get_spam('foo')
b = get_spam('bar')
print(a is b)

c = get_spam('foo')
print(a is c)
print()

"""
Writing a special factory function is often a simple approach for altering the normal
rules of instance creation. Once question that often arises at this point is whether
or not a more elegant approach could be taken.

Eg: you might consider a solution that redefines the __new__() method of a class as follows:
"""

import weakref

class Spam:
    _spam_cache = weakref.WeakValueDictionary()
    def __new__(cls, name):
        if name is cls._spam_cache:
            return cls._spam_cache[name]
        else:
            self = super().__new__(cls)
            cls._spam_cache[name] = self
            return self

    def __init__(self, name) -> None:
        print("Initializing SPAM")
        self.name = name

# At first glance, it seems like this code might do the job. However, a major problem is
# that the __init__() method always gets called, regardless of whether the instance was
# cached or not.
s = Spam("Dave")
t = Spam("Dave")
print(s is t)

# That behavior is probably not what you want. So, to solve the problem of caching without
# re-initialization, you need to take a slightly different approach.

# One immediate concern with this recipe might be its reliance on global variables and a
# factory function that's decoupled from the original class definition. One way to clean
# this up is to put the caching code into a spearate manager class and glue things together
# like this:

import weakref

class CachedSpamManager:
    def __init__(self) -> None:
        self._cache = weakref.WeakValueDictionary()

    def get_spam(self, name):
        if name not in self._cache:
            s = Spam(name)
            self._cache[name] = s
        else:
            s = self._cache[name]
        return s

    def clear(self):
        self._cache.clear()

class Spam:
    manager = CachedSpamManager()

    def __init__(self, name) -> None:
        self.name = name

def get_spam(name):
    return Spam.manager.get_spam(name)

a = Spam('foo')
b = Spam('foo')
print(a is b)

"""
If preventing this is important, you can take certain steps to avoide it.
Eg: You might give the class a name starting with an underscore, such as _Spam, which
    at least gives the user a clue that they shouldn't access it directly.

    Alternatively, if you want to give users a stronger hint that they shouldn't
    instantiate Spam instances directly, you can make __init__() raise an exception
    and use a class method to make an alternate constructor like this:
"""
class Spam:
    def __init__(self, *args, **kwargs) -> None:
        raise RuntimeError("Can't instantiate directly")

    # Alternate constructor
    @classmethod
    def _new(cls, name):
        self = cls.__new__(cls)
        self.name = name

# To use this, you modify the caching code to use Spam._new() to create instances
# instead of the usual call to Spam()

import weakref

class CachedSpamManager:
    def __init__(self) -> None:
        self._cache = weakref.WeakValueDictionary()

    def get_spam(self, name):
        if name not in self._cache:
            s = Spam._new(name) # Modified creation
            self._cache[name] = s
        else:
            s = self._cache[name]
        return s
