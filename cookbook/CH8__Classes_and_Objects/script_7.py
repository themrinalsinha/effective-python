"""
8.10. Using Lazily Computed Properties

Problem: You'd like to define a read-only attribute as a property that only gets
         computed on access. However, once accessed, you'd like the value to be
         cached and not recomputed on each access.

Solution: An efficient way to define a lazy attribute is through the use of a descriptor
          class, such as the following.
"""

class lazyproperty:
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            value = self.func(instance)
            setattr(instance, self.func.__name__, value)
            return value

# To utilize this code, you would use it in a class such as the following
import math

class Circle:
    def __init__(self, radius) -> None:
        self.radius = radius

    @lazyproperty
    def area(self):
        print('Computing area')
        return math.pi * self.radius ** 2

    @lazyproperty
    def perimeter(self):
        print('Computring perimeter')
        return 2 * math.pi * self.radius

c = Circle(4.0)
print(f"RADIUS: {c.radius}")
print(f"area: {c.area}")
print(f"perimeter: {c.perimeter}")
print(f"area: {c.area}")
print(f"perimeter: {c.perimeter}")
print(f"area: {c.area}")
print(f"perimeter: {c.perimeter}")

c = Circle(8.0)
print(f"RADIUS: {c.radius}")
print(f"area: {c.area}")
print(f"perimeter: {c.perimeter}")
print(f"area: {c.area}")
print(f"perimeter: {c.perimeter}")
print(f"area: {c.area}")
print(f"perimeter: {c.perimeter}")
# Carefully observe that the messages “Computing area” and “Computing perimeter” only
# appear once.
