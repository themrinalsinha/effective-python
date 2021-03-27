"""
Item 47: Use __getattr__, __getattribute__, and __setattr__ for lazy attributes

Python's object hooks make it easy to write generic code for gluing systems together.

Eg: say that i want to represent the records in a database as Python objects.
    The database has its schema set already. My code that uses objects corresponding
    to those records must also know what the database looks like. However, in python,
    the code that connects python objects to the database doesn't need to explicitly
    specify the schema of the records; it can be generic.

How is that possible:
- Plain instance attributes, @property methods and descriptors can't do that because
  they all need to be defined in advance. Python makes this dynamic behavior possible
  with the __getter__ special method. If a class defines __getattr__, that method is
  called every time an attribute can't be found in an object's instance dictionary
"""
# NOTE: Important
class LazyRecord:
    def __init__(self):
        self.exists = 5

    def __getattr__(self, name):
        value = f'Value for {name}'
        setattr(self, name, value)
        return value
# Here, I access the missing property foo. This causes Python to call the __getattr__
# method above, which mutates the instance dictionary __dict__
data = LazyRecord()
print('Before: ', data.__dict__)

print('foo   : ', data.foo)
print('After : ', data.__dict__)

print('foo   : ', data.bar)
print('After : ', data.__dict__)

print('foo   : ', data.random)
print('After : ', data.__dict__)

# ------------------------------------------------------------------------------------
# Here let's add logging to LazyRecord to show when __getter__ is actually called.
# Note how i call super().__getattr__() to use the super classes implementation of
# __getattr__ in order to fetch the real property value and avoid infinite recursion

class LoggingLazyRecord(LazyRecord):
    def __getattr__(self, name):
        print(f"👄 called __getattr__({name!r}), populating instance dictionary")
        result = super().__getattr__(name)
        print(f"👅 returning {result!r}")
        return result

data = LoggingLazyRecord()
print('Exists:     ', data.exists)
print('First foo:  ', data.foo)
print('Second foo: ', data.foo)
# -------------------------------------------------------------------------------------

"""
This behavior is especially helpful for use cases like lazily accessing
schemaless data. __getattr__ runs once to do the hard work of load-
ing a property; all subsequent accesses retrieve the existing result.
Say that I also want transactions in this database system. The next
time the user accesses a property, I want to know whether the cor-
responding record in the database is still valid and whether the
transaction is still open. The __getattr__ hook won’t let me do this
reliably because it will use the object’s instance dictionary as the fast
path for existing attributes.
"""

# To enable this more advanced use case, Python has another object hook called
# __getattribute__. This special method is called every time an attribute is accessed
# on an object, even in cases where it doesn't exist in the attribute dictionary.

# This enables me to do things like check global transaction state on every property
# access. It's important to note that such an operation can incur significant overhead
# and negativity impact performace, but sometimes it's worth it.

class ValidatingRecord:
    def __init__(self) -> None:
        self.exists = 5

    def __getattribute__(self, name):
        print(f'💎 called __getattribute__({name!r})')
        try:
            value = super().__getattribute__(name)
            print(f'💎 found {name!r}, returning {value!r}')
            return value

        except AttributeError:
            value = f"🙆 value for {name}"
            print(f"💎 setting {name!r} to {value!r}")
            setattr(self, name, value)
            return value

data = ValidatingRecord()
print('Exists:      ', data.exists)
print('first foot:  ', data.foo)
print('second foot: ', data.foo)

# In the event that a dynamically accessed property shouldn't exist, I can raise
# an AttributeError to cause Python's standard missing property behavior for both
# __getattr__ and __getattribute__

class MissingPropertyRecord:
    def __getattr__(self, name):
        if name == 'bad_name':
            raise AttributeError(f"{name} is missing")

data = MissingPropertyRecord()
# data.bad_name

# =====================================================================================
# Now, say i want to lazily push data back to the database when values are assigned to my
# python object. I can do this with __setattr__, a similar object hook that lets you intercept
# arbitrary attribute assignments. Unlike when retrieving an attribute with __getattr__ and
# __getattribute__, there's no need for two separate methods. The __setattr__ method is always
# called every time an attribute is assigned on an instance (either directly or through the
# setattr built-in function)

class SavingRecord:
    def __setattr__(self, name, value):
        # save some data for the record
        super().__setattr__(name, value)

# Here, I define a logging subclass of SavingRecord. Its __setattr__ method is always
# called on each attribute assignment

class LoggingSavingRecord(SavingRecord):
    def __setattr__(self, name, value):
        print(f'* called __setattr__({name!r}, {value!r})')
        return super().__setattr__(name, value)

data = LoggingSavingRecord()
print('Before: ', data.__dict__)
data.foo = 5
print('After: ', data.__dict__)
data.foo = 7
print('Finally: ', data.__dict__)

# The problem with __getattribute__ and __setattr__ is that they’re
# called on every attribute access for an object, even when you may not
# want that to happen. For example, say that I want attribute accesses
# on my object to actually look up keys in an associated dictionary

class BrokenDictionaryRecord:
    def __init__(self, data) -> None:
        self._data = {}

    def __getattribute__(self, name: str):
        print(f"* called __getattribute__({name!r})")
        return self._data[name]

# data = BrokenDictionaryRecord({'foo': 3})
# data.foo
# Max recursion depth reached...

# The problem is that __getattribute__ accesses self._data , which
# causes __getattribute__ to run again, which accesses self._data
# again, and so on. The solution is to use the super().__getattribute__
# method to fetch values from the instance attribute dictionary. This
# avoids the recursion:

class DictionaryRecord:
    def __init__(self, data) -> None:
        self._data = data

    def __getattribute__(self, name):
        print(f'called __getattribute__({name!r})')
        data_dict = super().__getattribute__('_data')
        return data_dict[name]

# data = DictionaryRecord({'foo', 3})
# print('foo: ', data.foo)

"""
Things to Remember
✦ Use __getattr__ and __setattr__ to lazily load and save attributes
  for an object.
✦ Understand that __getattr__ only gets called when accessing a
  missing attribute, whereas __getattribute__ gets called every time
  any attribute is accessed.
✦ Avoid infinite recursion in __getattribute__ and __setattr__
  by using methods from super() (i.e., the object class) to access
  instance attributes.
"""
