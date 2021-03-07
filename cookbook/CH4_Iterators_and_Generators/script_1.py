"""
4.1. Manually Consuming an Iterator

Problem: You need to process items in an iterable, but for whatever reason, you can't
         or don't want to use a for loop

Solution: To manually consume an iterable, use the next() function and write you code
          to catch the StopIteration exception.
"""
with open("/etc/passwd") as f:
    try:
        while True:
            line = next(f)
            print(line, end="")
    except StopIteration:
        pass

# Or, without catching exception
with open('/etc/passwd') as f:
    while True:
        line = next(f, None)
        if line is None:
            break
        print(line, end="")

print('- ' * 50)
# ====================================================================================

"""
4.2 Delegating Iteration

Problem: You have built a custom container object that internally holds a list, tuple or
         some other iterable. You would like to make iteration work with your new container

Solution: Typically, all you need to do is define an __iter__() method that delegates iteration
          to the internally held container.
"""

class Node:
    def __init__(self, value) -> None:
        self._value = value
        self._children = []

    def __repr__(self) -> str:
        return f'Node({self._value})'

    def add_child(self, node):
        self._children.append(node)

    def __iter__(self):
        return iter(self._children)

root    = Node(0)
child_1 = Node(1)
child_2 = Node(2)
child_3 = Node(3)
child_4 = Node(4)
child_5 = Node(5)

root.add_child(child_1)
root.add_child(child_2)
root.add_child(child_3)
root.add_child(child_4)
root.add_child(child_5)

for _node in root:
    print(_node)
print("- " * 50)
# =====================================================================================

"""
4.3. Creating New Iteration Pattern with Generators

Problem: You want to implement a custom iteration pattern that's different than the usual
         built-in functions (eg: range(), reversed() etc.)

Solution: If you want to implement a new kind of iteration pattern, define it using a generator
          function. Here's a generator that produces a range of floating-point numbers.
"""
def frange(start, stop, increment):
    x = start
    while x < stop:
        yield x
        x += increment

# To use such a function, you iterate over it using a for loop or use it with some other
# function that consumes an iterable (eg: sum(), list() etc)
for n in frange(0, 4, 0.5):
    print(n)

print(list(frange(0, 1, 0.125)))
print("- " * 50)
# ======================================================================================

"""
4.4. Implementing the Iterator Protocol

Problem: You are building custom objects on which you would like to support iteration, but
         would like an easy way to implement the iterator protocol.

Solution: By far, the easiest way to implement iterator on an object is to use a generator
          function.
"""
class Node:
    def __init__(self, value) -> None:
        self._value    = value
        self._children = []

    def __repr__(self) -> str:
        return f"Node({self._value})"

    def add_child(self, node):
        self._children.append(node)

    def __iter__(self):
        return iter(self._children)

    def depth_first(self):
        yield self
        for c in self:
            yield from c.depth_first()

root = Node(0)
child_1 = Node(1)
child_2 = Node(2)
child_3 = Node(3)
child_4 = Node(4)

root.add_child(child_1)
root.add_child(child_2)
root.add_child(child_3)
root.add_child(child_4)

for ch in root.depth_first():
    print("--> ", ch)

# In this code, the depth_first() method is simple to read and describe. It first yields
# itself and then iterates over each child yielding the items produced by the child’s
# depth_first() method (using yield from ).
print('- ' * 50)
# =====================================================================================

"""
4.6 Defining Generator Functions with Extra State

Problem: You would like to define a generator function, but it involves extra state that
         you would like to expose to the user somehow.

Solution: If you want to generator to expose extra state to the user, don't forget that you
          can easily implement it as a class, putting the generator function code in the
          __iter__() method.
"""
from collections import deque

class linehistory:
    def __init__(self, lines, histlen=3) -> None:
        self.lines = lines
        self.history = deque(maxlen=histlen)

    def __iter__(self):
        for lineno, line in enumerate(self.lines, 1):
            self.history.append((lineno, line))
            yield line

    def clear(self):
        self.history.clear()
