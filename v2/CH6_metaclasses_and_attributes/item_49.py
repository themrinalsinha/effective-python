"""
Item 49: Register class existence with __init_subclass__

Another common use of metaclasses is to automatically register types in a program.
Registration is useful for doing reverse lookups, where you need to map a simple
identifier back to a corresponding class.
"""

# Eg: say that i want to implement my own serialized representation of a Python object
# using JSON. I need a way to turn an object into a JSON string. Here, I do this generically
# by defining a base class that records the constructor parameters and turns them into a
# JSON dictionary:

import json

class Serializable:
    def __init__(self, *args) -> None:
        self.args = args

    def serializer(self):
        return json.dumps({'args': self.args})

# This class makes it easy to serialize simple, immutable data structure like
# Point2D to a string:

class Point2D(Serializable):
    def __init__(self, x, y) -> None:
        super().__init__(x, y)
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f'Point2D({self.x}, {self.y})'

point = Point2D(5, 3)
print('Object     : ', point)
print('Serialized : ', point.serializer())


# Now, I need to deserialize the JSON string and construct the Point2D object it
# represents. Here, I define another class that can deserialize the data from its
# Serializable parent class...

class Deserializable(Serializable):
    def __init__(self, x, y) -> None:
        super().__init__(x, y)
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f'Point2D({self.x}, {self.y})'

point = Point2D(5, 3)
print('\nobject     : ', point)
print('serialized : ', point.serializer())
# ======================================================================================

# Now, I need to deserialize this JSON string and construct the Point2D object it
# represents. Here I define another class that can deserialize the data from its
# Serializable parent class:

class Deserializable(Serializable):
    @classmethod
    def deserialize(cls, json_data):
        params = json.loads(json_data)
        return cls(*params['args'])

# Using Deserializable makes it easy to serialize and deserialize simple, immutable
# objects in a generic way:
# ======================================================================================

class BetterSerializable:
    def __init__(self, *args):
        self.args = args

    def serialize(self):
        return json.dumps({
            'class': self.__class__.__name__,
            'args': self.args,
        })

    def __repr__(self) -> str:
        name = self.__class__.__name__
        args_str = ', '.join(str(x) for x in self.args)
        return f'{name}({args_str})'

# Then, I can maintain a mapping of class names back to constructors for those objects.
# The general deserialize function works for any classes passed to register_class:

registry = {}

def register_class(target_class):
    registry[target_class.__name__] = target_class

def deserialize(data):
    params = json.loads(data)
    name = params['class']
    target_class = registry[name]
    return target_class(*params['args'])

# To ensure that deserialize always works properly, I must call register_class for
# every class I may want to deserialize in the future:

class EvenBetterPoint2D(BetterSerializable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y

register_class(EvenBetterPoint2D)

# Now, I can deserialize an arbitrary JSON string without having to know which class
# it contains:
before = EvenBetterPoint2D(5, 3)
print('Before: ', before)
data = before.serialize()
print('Serialized: ', data)
after = deserialize(data)
print('After: ', after)
# ======================================================================================

class Meta(type):
    def __new__(meta, name, bases, class_dict):
        cls = type.__new__(meta, name, bases, class_dict)
        register_class(cls)
        return cls

class RegisteredSerializable(BetterSerializable, metaclass=Meta):
    pass

# When i define a subclass of RegisteredSerializable, I can be confident that the call
# to register_class happend and deserialize will always work as expected:

class Vector3D(RegisteredSerializable):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)
        self.x, self.y, self.z = x, y, z

before = Vector3D(10, -7, 3)
print('Before: ', before)
data = before.serialize()

print('Serialized: ', data)
print('After: ', deserialize(data))
# ========================================================================================

# An even better approach is to use the __init_subclass__ special class method. This
# simplified syntax, introduced in python 3.6, reduces the visual noise of applying custom
# logic when a class is defined. It also makes it more approachable to beginners who may be
# confused by the complexity of metaclass syntax:

class BetterRegisteredSerializable(BetterSerializable):
    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        register_class(cls)

class Vector1D(BetterRegisteredSerializable):
    def __init__(self, magnitude):
        super().__init__(magnitude)
        self.magnitude = magnitude

before = Vector1D(6)
print('Before: ', before)
data = before.serialize()
print('Serialized: ', data)
print('After: ', deserialize(data))

# By using __init_subclass__ (or metaclasses) for class registration, you can ensure
# that you'll never miss registering a class as long as the inheritance tree is right.
# This works well for serialization, as I've shown, and also applies to database
# object-relational mappings (ORMs), extensible plug-in system, and callback hooks

"""
Things to Remember

✦ Class registration is a helpful pattern for building modular Python
  programs.

✦ Metaclasses let you run registration code automatically each time a
  base class is subclassed in a program.

✦ Using metaclasses for class registration helps you avoid errors by
  ensuring that you never miss a registration call.

✦ Prefer __init_subclass__ over standard metaclass machinery
  because it’s clearer and easier for beginners to understand.
"""
