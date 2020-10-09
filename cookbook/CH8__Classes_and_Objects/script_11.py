"""
8.14. Implementing custom containers

Problem: you want to implement a custom class that mimics the behavior of a common built-in
         container type, such as a list or dictionary. However, you're not entirely sure what
         methods need to be implemented to do it.

Solution: The collections library defines a variety of abstract classes that are extremely useful
          when implementing custom container classes. To illustrate, suppose you want you class to
          support iteration. To do that, simply start by having it inherit from collections.Iterable
"""

from collections.abc import Iterable, Sequence, MutableSequence

class A(Iterable):
    pass

# The special feature about inheriting from collections.Iterable is that it ensures you
# implement all of the required special methods. If you don’t, you’ll get an error upon
# instantiation

# Other notable classes defined in collections include Sequence , MutableSequence ,
# Mapping , MutableMapping , Set , and MutableSet . Many of these classes form hierarchies
# with increasing levels of functionality (e.g., one such hierarchy is Container , Itera
# ble , Sized , Sequence , and MutableSequence ). Again, simply instantiate any of these
# classes to see what methods need to be implemented to make a custom container with
# that behavior

import bisect

class SortedItems(Sequence):
    def __init__(self, initial=None) -> None:
        self._items = sorted(initial) if initial else []

    # required sequence methods
    def __getitem__(self, index):
        return self._items[index]

    def __len__(self) -> int:
        return len(self._items)

    # method for adding an item in the right location
    def add(self, item):
        bisect.insort(self._items, item)

items = SortedItems([5, 1, 3])
print(list(items))
items.add(-10)
print(list(items))

"""
Many of the abstract base classes in collections also provide default implementations
of common container methods. To illustrate, suppose you have a class that inherits from
collection MutableSequence, like this
"""
class Items(MutableSequence):
    def __init__(self, initial=None) -> None:
        self._items = list(initial) if initial else []

    # required sequence methods
    def __getitem__(self, index):
        print(f"Getting: {index}")
        return self._items[index]

    def __setitem__(self, index, value):
        print(f"Setting: {index},{value}")
        self._items[index] = value

    def __delitem__(self, index):
        print(f"Deleting: {index}")
        del self._items[index]

    def insert(self, index, value):
        print(f'Inserting: {index} -> {value}')
        self._items.insert(index, value)

    def __len__(self):
        print("Len")
        return len(self._items)

a = Items([1, 2, 3])
print(len(a))

a.append(4)
a.count(2)
a.remove(3)
