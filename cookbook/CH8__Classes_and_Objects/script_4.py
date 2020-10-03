"""
8.7. calling a method on a parent class

Problem: you want to invoke a method in a parent class in place of a method
        that has been overridden in a subclass.

Solution: to call a method in a parent (or superclass), use the super() function.
"""

class A:
    def spam(self):
        print('A.spam')

class B(A):
    def spam(self):
        print('B.spam')
        super().spam() # call parent spam()

# a very common use of super() is in the handling of the __init__() method
# to make sure that parents are properly initialized.
class A:
    def __init__(self) -> None:
        self.x = 0

class B(A):
    def __init__(self) -> None:
        super().__init__()
        self.y = 1

# another common use of super() is in code that override any of Python's
# special methods
class Proxy:
    def __init__(self, obj) -> None:
        self._obj = obj

    # delegate attribute lookup to internal obj
    def __getattr__(self, name):
        return getattr(self._obj, name)

    # delegate attribute assignment
    def __setattr__(self, name, value):
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            setattr(self._obj, name, value)

# the implementation of __setattr__() includes a name check. If the
# name starts with an underscore (_), it invokes the original implementation of
# __setattr__() using super() . Otherwise, it delegates to the internally held object
# self._obj . It looks a little funny, but super() works even though there is no explicit
# base class listed

# Correct use of the super() function is actually one of the most poorly understood
# aspects of Python. Occasionally, you will see code written that directly calls a method
# in a parent like this

class Base:
    def __init__(self) -> None:
        print('Base.__init__')

class A(Base):
    def __init__(self) -> None:
        Base.__init__(self)
        print('A.__init__')

# Although this “works” for most code, it can lead to bizarre trouble in advanced code
# involving multiple inheritance.

class Base:
    def __init__(self) -> None:
        print("Base.__init__")

class A(Base):
    def __init__(self) -> None:
        Base.__init__(self)
        print('A.__init__')

class B(Base):
    def __init__(self) -> None:
        Base.__init__(self)
        print('B.__init__')

class C(A, B):
    def __init__(self) -> None:
        A.__init__(self)
        B.__init__(self)
        print('C.__init__')


c = C()
print(f"MRO: {C.__mro__}")
print()

class Base:
    def __init__(self) -> None:
        print("Base.__init__")

class A(Base):
    def __init__(self) -> None:
        super().__init__()
        print('A.__init__')

class B(Base):
    def __init__(self) -> None:
        super().__init__()
        print('B.__init__')

class C(A, B):
    def __init__(self) -> None:
        super().__init__()
        print('C.__init__')

c = C()
print(f"MRO: {C.__mro__}")

# To understand why it works, we need to step back for a minute and discuss how Python
# implements inheritance. For every class that you define, Python computes what’s known
# as a method resolution order (MRO) list. The MRO list is simply a linear ordering of
# all the base classes

"""
To implement inheritance, Python starts with the leftmost class and works its way left-
to-right through classes on the MRO list until it finds the first attribute match.

The actual determination of the MRO list itself is made using a technique known as C3
Linearization. Without getting too bogged down in the mathematics of it, it is actually
a merge sort of the MROs from the parent classes subject to three constraints:
• Child classes get checked before parents
• Multiple parents get checked in the order listed.
• If there are two valid choices for the next class, pick the one from the first parent.


"""

print("- " * 50)
# =========================================================================================

