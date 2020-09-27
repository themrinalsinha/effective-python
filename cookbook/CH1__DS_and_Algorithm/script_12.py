"""
1.20. combining multiple mappings into a single mapping

problem: you have multiple dictionaries or mappings that you want to logically combine
         into a single mapping to perform certain operations, such as looking up values
         checking for the existence of keys.
"""

from collections import ChainMap

a = {'x': 1, 'z': 3 }
b = {'y': 2, 'z': 4 }

# Now suppose you want to perform lookups where you have to check both dictionaries
# (e.g., first checking in a and then in b if not found). An easy way to do this is to use the
# ChainMap class from the collections module.

c = ChainMap(a, b)
print(f"chainmap: {c}")
print(c['x']) # outputs 1 (from a)
print(c['y']) # outputs 2 (from b)
print(c['z']) # outputs 3 (from c)

# A "ChainMap" takes multiple mappings and makes them logically appear as one. however
# the mappings are not literally merged together. Insted, a ChainMap simply keeps a
# list of underlying mappings and redefines common dictionary operations to scan the list.
print(len(c), c.keys(), c.values())

# A ChainMap is particularly useful when working with scoped values such as variables in
# a programming language (i.e., globals, locals, etc.).

values = ChainMap()
values['x'] = 1
print(values)

values = values.new_child()
values['x'] = 2
print(values)

values = values.new_child()
values['x'] = 3
print(values)
print(f"x ==> {values['x']}")
values = values.parents
print(values)
print(f"x ==> {values['x']}")
values = values.parents
print(values)
print(f"x ==> {values['x']}")

# as an alternative to ChainMap, you might consider mergin dictionaries together using
# the update() method.
a = {'x': 1, 'z': 3}
b = {'y': 2, 'z': 4}
merged = dict(b)
merged.update(a)
print(f"merged dictionary: {merged}")
