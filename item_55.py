
"""
item 55: using repr string for debugging output

The print function outputs a human-readable string version of whatever you supply to it.
If you're debugging a program with print, the type difference matters. What you always
want is to see the repr version of an object. The repr built-in function returns the
printable representation of an object, which should be its most clearly understandable
string representation.
"""

x = '\x07'
print(f"PRINT -> {x}")
print(f"REPR -> {repr(x)}")

"""
Passing the value from repr to the eval built-in function should result in the same Python
object you started with (of course, in practice you should use eval with extreme cautious)
"""

b = eval(repr(x))
print(b)
print(repr(b))
assert x == b


"""
When you're debugging with print, you should repr the value before printing to ensure that
any difference in types is clear.
"""
print(f"5 as int: {repr(5)}")
print(f"5 as string: {repr('5')}")
print()
"""
For dynamic python objects, the default human-readable string value is the same as the repr value.
Unfortunately, the default value of repr for object instance isn't especially helpful.
"""

class OpaqueClass(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

obj_opaque = OpaqueClass(1, 2)
print(f"PRINTING CLASS OBJECT: {obj_opaque}")
print(f"PRINTING CLASS OBJECT(repr): {repr(obj_opaque)}")

"""
the output of print(obj) can't be  passed to the eval function, and it says nothing about the instance
fields of the object.

There are two solutions to this problem. If you have control of the class, you can define your own __repr__
special method that returns a string containing the python expression that recreates the object.
"""

class BetterClass(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'BetterClass({self.x}, {self.y})'

obj = BetterClass(1, 2)
print(f"PRINTING CLASS OBJECT: {obj}")
print(f"PRINTING CLASS OBJECT(repr): {repr(obj)}")

"""
When you don't have control over the class definition, you can reach into the object's instance directory,
which is stored in the __dict__ attribute, Here, I print out the content of an OpaqueClass instance.
"""
print('OF OpaqueClass')
print(obj_opaque.__dict__)
