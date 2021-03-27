"""
Item 48: Validate subclasses with __init_subclass__

One of the simplest applications of metaclasses is verifying that a class was defined
correctly. When you're building a complex class hierarchy, you may want to enforce style,
require overriding methhods, or have strict relationships between class attributes.
Metaclasses enable these use cases by providing a reliable way to run your validation
code each time a new subclass is defined.

Often a class’s validation code runs in the __init__ method, when an object of the
class’s type is constructed at runtime. Using metaclasses for validation can raise
errors much earlier, such as when the module containing the class is first imported
at program startup.

Before I get into how to define a metaclass for validating subclasses, it’s important
to understand the metaclass action for standard objects. A metaclass is defined by
inheriting from type . In the default case, a metaclass receives the contents of
associated class statements in its __new__ method. Here, I can inspect and modify
the class information before the type is actually constructed.
"""

class Meta(type):
    def __new__(meta, name, bases, class_dict):
        print(f"* Running {meta}.__new__ for {name}")
        print('Bases: ', bases)
        print(class_dict)
        return type.__new__(meta, name, bases, class_dict)

class MyClass(metaclass=Meta):
    stuff = 123

    def foo(self):
        pass

class MySubclass(MyClass):
    other = 567

    def bar(self):
        pass

"""
I can add functionality to the Meta.__new__ method in order to validate all the
parameters of an associated class before it's defined.
Eg: say that i want to represent any type of multisided polygon. I can do this by
    defining a special validating metaclass and using it in the base class of my
    polygon class hierarchy. Not that it's important not to apply the same validation
    to the base class:
"""
class ValidatePolygon(type):
    def __new__(meta, name, bases, class_dict):
        # only validate subclasses of the polygon class
        if bases:
            if class_dict['sides'] < 3:
                raise ValueError('Polygons need 3+ sides')
        return type.__new__(meta, name, bases, class_dict)

class Polygon(metaclass=ValidatePolygon):
    sides = None # must be specified by subclasses

    @classmethod
    def interior_angles(cls):
        return (cls.sides - 2) * 180

class Triangle(Polygon):
    sides = 3

class Rectangle(Polygon):
    sides = 4

class Nonagon(Polygon):
    sides = 9

print(Triangle.interior_angles())
print(Rectangle.interior_angles())
print(Nonagon.interior_angles())


# If I try to define a polygon with fewer than three sides, the validation will cause
# the class statement to fail immediately after the class statement body.
# print('before class')
# class Line(Polygon):
#     print('before side')
#     sides = 2
#     print('after side')
# print('after class')

# This seems like quite a lot of machinery in order to get Python to
# accomplish such a basic task. Luckily, Python 3.6 introduced simplified
# syntax—the __init_subclass__ special class method—for achieving
# the same behavior while avoiding metaclasses entirely. Here, I use
# this mechanism to provide the same level of validation as before:
class BetterPolygon:
    sides = None # must be specified by subclasses

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        if cls.sides < 3:
            raise ValueError('Polygons need 3+ sides')

    @classmethod
    def interior_angles(cls):
        return (cls.sides - 2) * 180

class Hexagon(BetterPolygon):
    sides = 6

print(Hexagon.interior_angles())

# The code is much shorter now, and the ValidatePolygon metaclass is
# gone entirely. It’s also easier to follow since I can access the sides
# attribute directly on the cls instance in __init_subclass__ instead of
# having to go into the class’s dictionary with class_dict['sides'] . If
# I define an invalid subclass of BetterPolygon , the same exception is
# raised
# ===========================================================================================

# Another problem with the standard Python metaclass machinery
# is that you can only specify a single metaclass per class definition.
# Here, I define a second metaclass that I’d like to use for validating the
# fill color used for a region (not necessarily just polygons):

class ValidateFilled(type):
    def __new__(meta, name, bases, cls_dict):
        # only validate subclasses of the filled class
        if bases:
            if cls_dict['color'] not in ('red', 'green'):
                raise ValueError('fill color must be supported')
        return type.__new__(meta, name, bases, cls_dict)

class Filled(metaclass=ValidateFilled):
    color = None # must be specified by subclass

# # When i try to use the polygon metaclass and filled metaclass together, i get a
# # cryptic error message:
# class RedPentagon(Filled, Polygon):
#     color = 'red'
#     sides = 5

# It is possible to fix this by creating a complex hierarchy of metaclasses type
# definitions to layer validation:
class ValidatePolygon(type):
    def __new__(meta, name, bases, class_dict):
        # only validate non-root classes
        if not class_dict.get('is_root'):
            if class_dict['sides'] < 3:
                raise ValueError('Polygons need 3+ sides')
        return type.__new__(meta, name, bases, class_dict)

class Polygon(metaclass=ValidatePolygon):
    is_root = True
    sides = None # Must be specified by subclasses

class ValidateFilledPolygon(ValidatePolygon):
    def __new__(meta, name, bases, class_dict):
        # only validate non-root classes
        if not class_dict.get('is_root'):
            if class_dict['color'] not in ('red', 'green'):
                raise ValueError('Filled color must be supported')
        return super().__new__(meta, name, bases, class_dict)

class FilledPolygon(Polygon, metaclass=ValidateFilledPolygon):
    is_root = True
    color = None # Must be specified by subclass

# this requires every FilledPolygon instance to be a Polygon instance:
class GreenPentagon(FilledPolygon):
    color = 'green'
    sides = 5

greenie = GreenPentagon()
assert isinstance(greenie, Polygon)

# class RedLine(FilledPolygon):
#     color = 'red'
#     sides = 2
# class RedLine(FilledPolygon):
#     color = 'orange'
#     sides = 2
# -----------------------------========================================================


# The __init_subclass__ special class method can also be used to
# solve this problem. It can be defined by multiple levels of a class
# hierarchy as long as the super built-in function is used to call any
# parent or sibling __init_subclass__ definitions (see Item 40: “Initial-
# ize Parent Classes with super ” for a similar example). It’s even com-
# patible with multiple inheritance. Here, I define a class to represent
# region fill color that can be composed with the BetterPolygon class
# from before

class Filled:
    color = None

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        if cls.color not in ('red', 'green', 'blue'):
            raise ValueError('fills need a valid color')

    # I can inherit from both classes to define a new class. Both classes call
    # super().__init_subclass__(), causing their corresponding validation logic
    # to run when the subclass is created:

class RedTriangle(Filled, Polygon):
    color = 'red'
    sides = 3

ruddy = RedTriangle()
print(isinstance(ruddy, Filled))
print(isinstance(ruddy, Polygon))
# =============================================================================================

"""
You can even use __init_subclass__ in complex cases like diamond inheritance. Here, I define
a basic diamond hierarchy to show this in action:
"""

class Top:
    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        print(f'Top for {cls}')

class Left(Top):
    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        print(f'Left for {cls}')

class Right(Top):
    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        print(f"Right for {cls}")

class Bottom(Left, Right):
    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        print(f'Bottom for {cls}')

# As expected, Top.__init_subclass__ is called only a single time for each class, even
# though there are two paths to it for the Bottom class through its Left and Right
# parent classes.

"""
Things to Remember
✦ The __new__ method of metaclasses is run after the class
  statement’s entire body has been processed.

✦ Metaclasses can be used to inspect or modify a class after it’s
  defined but before it’s created, but they’re often more heavyweight
  than what you need.

✦ Use __init_subclass__ to ensure that subclasses are well formed
  at the time they are defined, before objects of their type are
  constructed.

✦ Be sure to call super().__init_subclass__ from within your class’s
  __init_subclass__ definition to enable validation in multiple layers
  of classes and multiple inheritance.
"""
