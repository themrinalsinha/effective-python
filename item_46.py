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

# ================================================================================

# Default Dictionaries:
# Dictionaries are useful for bookkeeping and tracking statics. One problem with dictionaries is that
# you can't assume any keys are already present. That makes it clumsy to do simple things like increment a
# counter stored in a dictionary.

stats = {}
key = 'my_counter'
if key not in stats:
    stats[key] = 0
stats[key] += 1

# The defaultdict class from the collections module simplifies this by automatically storing a default value when
# a key doesn't exist. All you have to do is provide a function that ill return the default value each time a key
# is missing. In this example, the int built-in function returns 0. Now incrementing a counter is simple.

from collections import defaultdict

stats = defaultdict(int)
stats['my_counter'] += 1
stats['my_counter'] += 1
stats['my_counter'] += 1
print(stats)

# ================================================================================

# Heap Queue
# Heap is useful data structure for maintaining a priority queue.
# The head module provides functions for creaating heaps in standard list types
# with functions like heappush, heappop and nsmallest.

# Items of any priority can be inserted into the heap in any order.
from heapq import heappush, heappop, nsmallest
a = []
heappush(a, 5)
heappush(a, 3)
heappush(a, 7)
heappush(a, 4)
print(a)
# Items are always removed by highest priority(lowest number) first.
print(heappop(a))
print(heappop(a))
print(heappop(a))
print(heappop(a))

b = []
heappush(b, 5)
heappush(b, 3)
heappush(b, 7)
heappush(b, 4)
print(b)
print('first index of heap: ', b[0])

assert b[0] == nsmallest(1, b)[0] == 3

# calling the sort method on the list  maintains the heap invarient.
print('Before: ', b)
b = b.sort()
print('After: ', b)
# Each of these heapq operations takes logarithmic time in proportion to
# the length of the list. Doing the same worlk with a standard Python list would scale linearly.

# ================================================================================
# Bisection
# Searching for an item in a list takes linear time proportioanl to its length wheen you call the index method.
from time   import time
from bisect import bisect_left

x = list(range(10 ** 8))
start_time = time()
print(x.index(991234))
print("Liner time: ", time() - start_time)

# The bisect module's function, such as bisect_left, provide an efficient binary search through a sequence of sorted items.
# The index it  returns is the insertion point of the value into the sequence.
start_time = time()
print(bisect_left(x, 991234))
print("Bisect time: ", time() - start_time)

# ================================================================================
# Iterator Tools
# The itertools built-in module contains a large number of functions that are useful for organizing and interacting with iterators ()
