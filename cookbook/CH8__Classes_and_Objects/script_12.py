"""
8.15. Delegating Attribute Access

Problem: You want an instance to delegate attribute access to an internally held instance
         possibly as an alternative to inheritance or in order to implement a proxy.
"""

class A:
    def spam(self, x):
        pass

    def foo(self):
        pass

class B:
    def __init__(self):
        self._a = A()

    def spam(self, x):
        # delegate to internal self._a instance
        return self._a.spam(x)

    def foo(self):
        # delegate to the internal self._a instance
        return self._a.foo()

    def bar(self):
        pass

"""
If there are only a couple of methods to delegate, writing code such as that just given is
easy enough. However, if there are many methods to delegate, an alternative approach
is to define the __getattr__() method
"""
class A:
    def spam(self, x):
        pass

    def foo(self):
        pass

class B:
    def __init__(self):
        self._a = A()

    def bar(self):
        pass

    # expose all of the methods defined on class A
    def __getattr__(self, name):
        return getattr(self._a, name)

# The __getattr__() method is kind of like a catch-all for attribute lookup. It’s a method
# that gets called if code tries to access an attribute that doesn’t exist. In the preceding
# code, it would catch access to undefined methods on B and simply delegate them to A.

b = B()
b.bar()
b.spam(42)
# =======================================================================================

# Another example of delegation is in the implementation of proxies
# A proxy class that wraps around another object, but exposes it public attributes

class Proxy:
    def __init__(self, obj):
        self._obj = obj

    # delegate attribute lookup to internal obj
    def __getattr__(self, name):
        print(f'getattr: {name}')
        return getattr(self._obj, name)

    # delegate attribute assignment
    def __setattr__(self, name, value) -> None:
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            print('setattr: ', name, value)
            setattr(self._obj, name, value)

    # delegate attribute deletion
    def __delattr__(self, name: str) -> None:
        if name.startswith('_'):
            super().__delattr__(name)
        else:
            print('delattr: ', name)
            delattr(self._obj, name)

# To use this proxy class, you simply wrap it around another instance
class Spam:
    def __init__(self, x) -> None:
        self.x = x
    def bar(self, y):
        print('Spam.bar: ', self.x, y)

# create an instance
s = Spam(2)

# create a proxy around it
p = Proxy(s)
print(p.x)
p.bar(3)
p.x = 37
print(p.x)

# By customizing the implementation of the attribute access methods, you could cus‐
# tomize the proxy to behave in different ways (e.g., logging access, only allowing read-
# only access, etc.).

class ListLike:
    def __init__(self):
        self._items = []
    def __getattr__(self, name):
        return getattr(self._items, name)
    # Added special methods to support certain list operations
    def __len__(self):
        return len(self._items)
    def __getitem__(self, index):
        return self._items[index]
    def __setitem__(self, index, value):
        self._items[index] = value
    def __delitem__(self, index):
        del self._items[index]
