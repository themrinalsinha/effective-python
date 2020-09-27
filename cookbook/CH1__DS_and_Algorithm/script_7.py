"""
1.10. removing duplicates from a sequence while maintaining order

Problem: you want to eliminate the duplicate values in a sequence, but preserve the
         order of the remaining items.
"""

# if the values in the sequence are hasable, the problem can be easily solved using
# a set and a generator. eg:
def dedupe(items):
    seen = set()
    for item in items:
        if item not in seen:
            yield item
            seen.add(item)

a = [1, 5, 2, 1, 9, 1, 5, 10]
result = list(dedupe(a))
print(f'Result: {result}')

# This only works if the items in the sequence are hashable. If you are trying to eliminate
# duplicates in a sequence of unhashable types (such as dicts), you can make a slight
# change to this recipe, as follow

def dedupe(items, key=None):
    seen = set()
    for item in items:
        val = item if key is None else key(item)
        if val not in seen:
            yield item
            seen.add(val)

a = [ {'x':1, 'y':2}, {'x':1, 'y':3}, {'x':1, 'y':2}, {'x':2, 'y':4}]
result = list(dedupe(a, key=lambda d: (d['x'],d['y'])))
print(result)
result = list(dedupe(a, key=lambda d: d['x']))
print(result)

# This latter solution also works nicely if you want to eliminate duplicates based
# on the value of a single field or attribute or a larger data structure.
a = [1, 5, 2, 1, 9, 1, 5, 10]
print(f"removing dups using set (without preserving order): {set(a)}")

# The use of a generator function in this recipe reflects the fact that you might want the
# function to be extremely general purpose—not necessarily tied directly to list process‐
# ing. For example, if you want to read a file, eliminating duplicate lines, you could simply
# do this:

# with open(somefile, 'r') as f:
#     for line in dedupe(f):
#         ...
#         ...
