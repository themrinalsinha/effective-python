"""
8.16. Defining more than one constructor in a class

Problem: you're writing a class, but you want users to be able to create instances in more
         than the one way provided by __init__().
"""
import time

class Date:
    # primary constructor
    def __init__(self, year, month, day) -> None:
        self.year = year
        self.month = month
        self.day = day

    # alternate constructor
    @classmethod
    def today(cls):
        t = time.localtime()
        return cls(t.tm_year, t.tm_mon, t.tm_mday)

a = Date(2012, 12, 21)  # primary constructor
b = Date.today()        # alternate constructor
print(a, b)
print('- ' * 50)
# ===================================================================================

"""
8.17. Creating an Instance without Invoking init

Problem: You need to create an instance, but want to bypass the execution of the
         __init__() method for some reason.
"""

class Date:
    def __init__(self, year, month, day) -> None:
        self.yar   = year
        self.month = month
        self.day   = day

# Here's how you can create a Date instance without invoking __init__()
d = Date.__new__(Date)
print(d)

data = {'year': 2012, 'month': 8, 'day': 29}
for key, value in data.items():
    setattr(d, key, value)

print(d.year)
print(d.month)
print('- ' * 50)
# ===================================================================================

"""
8.18. Extending classes with Mixins

Problem: you have a collection of generally useful methods that you like to make available
         for extending the functionality of other class definitions. However, the classes
         where the methods might be added aren't necessarily related to one another via inheritance.
         Thus, you can't just attach the methods to a common base class.
"""

class LoggedMappingMixin:
    """
    Add logging to get/set/delete operations for debugging
    """
    __slots__ = ()

    def __getitem__(self, key):
        print(f'Getting: {str(key)}')
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        print(f'Setting: {key} = {value}')
        return super().__setitem__(key, value)

    def __delitem__(self, key):
        print(f'Deleting: {str(key)}')
        return super().__delitem__(key)

class SetOnceMappingMixin:
    """
    Only allow a key to be set once
    """
    __slots__ = ()

    def __setitem__(self, key, value):
        if key in self:
            raise KeyError(str(key) + ' already set')
        return super().__setitem__(key, value)

class StringKeysmappingMixin:
    """
    Restrict keys to strings only
    """
    __slots__ = ()

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise TypeError("keys must be strings")
        return super().__setitem__(key, value)

class LoggedDict(LoggedMappingMixin, dict):
    pass

d = LoggedDict()
d['x'] = 23
d['x']
del d['x']
# ===================================================================================

from collections import defaultdict, OrderedDict

class SetOnceDefaultDict(SetOnceMappingMixin, defaultdict):
    pass

d = SetOnceDefaultDict(list)
d['x'].append(2)
d['y'].append(3)
d['x'].append(4)


class StringOrderedDict(StringKeysmappingMixin, SetOnceMappingMixin, OrderedDict):
    pass

d = StringOrderedDict()
d['x'] = 23
# d[42] = 10 # will throw type error

