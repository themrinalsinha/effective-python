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


