"""
8.24. Making Classes Support Comparison Operations

Problem: You'd like to be able to compare instances of your class using the standard
         comparison operators (eg: >=, !=, <=, etc.), but without having to write a
         lot of special methods.

Solution: Python classes can support comparison by implementing a special method for each
          comparison operator. Eg: to support >= you define __ge__() method in class.

          The functools.total_ordering decorator can be used to simplify the process.
          To use it, you decorate a class with it, and define __eq__() and one other
          comparison method (__lt__, __le__, __gt__, __ge__)
"""

from functools import total_ordering

class Room:
    def __init__(self, name, length, width) -> None:
        self.name = name
        self.length = length
        self.width = width
        self.square_feet = self.length * self.width

@total_ordering
class House:
    def __init__(self, name, style) -> None:
        self.name = name
        self.style = style
        self.rooms = list()

    @property
    def living_space_footage(self):
        return sum(r.square_feet for r in self.rooms)

    def add_room(self, room):
        self.rooms.append(room)

    def __str__(self) -> str:
        return f"{self.name}: {self.living_space_footage} square foot {self.style}"

    def __eq__(self, o: object) -> bool:
        return self.living_space_footage == o.living_space_footage

    def __lt__(self, o: object) -> bool:
        return self.living_space_footage < o.living_space_footage

"""
Here, the House class has been decorated with @total_ordering . Definitions of
__eq__() and __lt__() are provided to compare houses based on the total square
footage of their rooms. This minimum definition is all that is required to make all of
the other comparison operations work.
"""
h1 = House('h1', 'Cape')
h1.add_room(Room("Master Bedroom", 14, 21))
h1.add_room(Room("Living Room", 18, 20))
h1.add_room(Room("Kitchen", 12, 16))
h1.add_room(Room("Office", 12, 12))

h2 = House('h2', 'Ranch')
h2.add_room(Room("Master Bedroom", 14, 21))
h2.add_room(Room("Living Room", 18, 20))
h2.add_room(Room("Kitchen", 12, 16))

h3 = House('h3', 'Split')
h3.add_room(Room("Master Bedroom", 14, 21))
h3.add_room(Room("Living Room", 18, 20))
h3.add_room(Room("Kitchen", 15, 17))
h3.add_room(Room("Office", 12, 16))

houses = [h1, h2, h3]

print(f"Is H1 bigger than H2: {h1 > h2}")
print(f"Is H1 bigger than H2: {h2 < h3}")
print(f"Is H2 greater than or equal to H1: {h2 >= h1}")
print(f"Which one is biggest: {max(houses)}")
print(f"Which is smallest: {min(houses)}")


# Methods created by @total_ordering
# __le__ = lambda self, other: self < other or self == other
# __gt__ = lambda self, other: not (self < other or self == other)
# __ge__ = lambda self, other: not (self < other)
# __ne__ = lambda self, other: not self == other
