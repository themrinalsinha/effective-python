"""
8.23: Managing memory in cyclic data structures

Problem: You program creates data structures with cycles (eg. trees, graphs, observer pattern etc.)
         but you are experiencing problems with memory management

Solution: A simple example of a cyclic data structure is a tree structure where a parent points to
its children and the children point back to their parent. For code like this, you should
consider making one of the links a weak reference using the weakref library.
"""
import weakref

class Node:
    def __init__(self, value) -> None:
        self.value = value
        self._parent = None
        self.children = []

    def __repr__(self) -> str:
        return 'Node({!r:})'.format(self.value)

    # property that manages the parent as a weak-reference
    @property
    def parent(self):
        return self._parent if self._parent is None else self._parent()

    @parent.setter
    def parent(self, node):
        self._parent = weakref.ref(node)

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

# This implementation allows the parent to quietly die.
root = Node('parent')
c1 = Node('child')
root.add_child(c1)
print(c1.parent)

del root
print(c1.parent)
