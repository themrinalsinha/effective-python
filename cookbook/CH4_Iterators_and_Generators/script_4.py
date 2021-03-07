"""
4.14. Flattening a Nested Sequence

Problem: The is easily solved by writing a recursize generator function involving
         a yield from statement.
"""

from collections import Iterable

def flatten(items, ignore_types=(str, bytes)):
    for item in items:
        if isinstance(item, Iterable) and not isinstance(item, ignore_types):
            yield from flatten(item)
        else:
            yield item

items = [1, 2, [3, 4, [5, 6, [7, 8, [9]]]], 10, 11, [[[12]]]]
for x in flatten(items):
    print(x, end=' ')

# In the code, the isinstance(x, Iterable) simply checks to see if an item is iterable.
# If so, yield from is used to emit all of its values as a kind of subroutine. The end result
# is a single sequence of output with no nesting.

# The yield from statement is a nice shortcut to use if you ever want to write generators
# that call other generators as subroutines. If you don’t use it, you need to write code that
# uses an extra for loop. For example:
# def flatten(items, ignore_types=(str, bytes)):
#   for x in items:
#       if isinstance(x, Iterable) and not isinstance(x, ignore_types):
#           for i in flatten(x):
#               yield i
#       else:
#           yield x
#
# Although it’s only a minor change, the yield from statement just feels better and leads
# to cleaner code.

print()
# ==========================================================================================

"""
4.15. Iterating is sorted order over merged sorted iterables

Problem: You have a collection of sorted sequences and you want to iterate over a sorted
         sequence of them all merged together.

Solution: The heapq.merge() function does exactly what you want.
"""
import heapq

a = [1, 4, 7, 10]
b = [2, 5, 6, 11]

for c in heapq.merge(a, b):
    print(c)
print()
# =========================================================================================


"""
4.16. Replacing Infinite while loops with an iterator

Problem: You have code that uses a while loop to iteratively process data because it involves a
         function or some kind of unusual test condition that doesn't fall into the usual iteration
         pattern.
"""

# CHUNKSIZE = 8192

# def reader(s):
#     while True:
#         data = s.recv(CHUNKSIZE)
#         if data == b'':
#             break
#         process_data(data)

# def reader(s):
#     for chunk in iter(lambda: s.recv(CHUNKSIZE), b''):
#         process_data(data)

import sys
f = open('/etc/passwd')
for chunk in iter(lambda: f.read(10), ''):
    n = sys.stdout.write(chunk)
