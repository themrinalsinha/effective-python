# Use Built-In algorithms and datastructures

# The Python Standard Library has many of the algorithms and data structures you'll need to use built in.
# Besides speed, using these common algorithms and data structures can make your life easier.

# DOUBLE ENDED QUEUE:
# The deque class from the collections module is a double ended queue.
# It provides constant time operations for inserting or removing items from its beginning or end.
# This makes it ideal for first-in-first-out (FIFO) queues.

from collections import deque

fifo = deque()
fifo.append(1) # Producer
fifo.append(5) # Producer
fifo.append(9) # Producer
print(fifo)

x = fifo.popleft() # Consumer - Pop element from left
y = fifo.pop()     # Consumer - Pop element from right

# The list built-in type also contains an ordered sequence of items like a queue.
# You can insert or remove items from the end of a list in constant time.
# but inserting or removing itmes from the head fo a list takes linear time.
# which is much slower than the constant tie of a deque.
# ================================================================================

# ORDERED DICTIONARY
# Standard dictionaries are unordered. That means a dict with a same key and values
# can result in different orders of iterations. This behavior is a surprising by product
# of the way the dictionary's fast hash table is implemeted.

a = {}
a['foo'] = 1
a['bar'] = 2

# Randomly populate b to cause hash conflicts.
from random import randint
while True:
    z = randint(99, 1013)
    b = {}
    for i in range(z):
        b[i] = i
    b['foo'] = 1
    b['bar'] = 2

    for i in range(z):
        del b[i]
    if str(b) != str(a):
        break
print(a)
print(b)

# The OrderedDict class from collections module is a special type of dictionary that keeps
# track of the order in which itss keys were inserted. Iterating the keys of an OrderedDict
# has predictable behavior. This can vastly simplify testingg and debbing by making all code deterministic.

from collections import OrderedDict

a = OrderedDict()
a['foo'] = 1
a['bar'] = 2
print(a)
b = OrderedDict()
b['foo'] = 'red'
b['bar'] = 'blue'
for v1, v2 in zip(a.values(), b.values()):
    print(v1, v2)
