"""
1.5. implementing a priority queue

Problem: You want to implement a queue that sorts items by a given priority and
         always returns the item with the highest priority on each pop operation.

Solution: the following class uses the heapq module to implement the simple priority queue.
"""

import heapq

class PriorityQueue(object):
    def __init__(self) -> None:
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]

class Item(object):
    def __init__(self, name) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f'Item({self.name!r})'

q = PriorityQueue()
q.push(Item('foo'), 1)
q.push(Item('bar'), 5)
q.push(Item('jon'), 4)
q.push(Item('doe'), 1)

print(f"1. q.pop() --> {q.pop()}")
print(f"2. q.pop() --> {q.pop()}")
print(f"3. q.pop() --> {q.pop()}")
print(f"4. q.pop() --> {q.pop()}")

"""
The core of this recipe concerns the use of the heapq module. The functions heapq.heap
push() and heapq.heappop() insert and remove items from a list _queue in a way such
that the first item in the list has the smallest priority. The heappop() method always
returns the “smallest” item, so that is the key to making the
1.5. Implementing a Priority Queue queue pop the correct items. Moreover, since the push and pop operations have O(log
N) complexity where N is the number of items in the heap, they are fairly efficient even
for fairly large values of N.

In this recipe, the queue consists of tuples of the form (-priority, index, item) . The
priority value is negated to get the queue to sort items from highest priority to lowest
priority. This is opposite of the normal heap ordering, which sorts from lowest to highest
value.

The role of the index variable is to properly order items with the same priority level.
By keeping a constantly increasing index, the items will be sorted according to the order
in which they were inserted. However, the index also serves an important role in making
the comparison operations work for items that have the same priority level.
"""
