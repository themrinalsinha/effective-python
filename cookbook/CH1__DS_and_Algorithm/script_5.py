"""
1.6. mapping keys to multiple values in a dictionary

Problem: you want to make a dictionary that maps keys to more than one value (a so called multidict)

Solution: a dictionary is a mapping where each key is mapped to a single value, if you
          want to map keys to multiple values, you need to store the multiple values in
          another container such as a list or set.
"""

d = {
    'a' : [1, 2, 3],
    'b' : [4, 5]
}

e = {
    'a' : {1, 2, 3},
    'b' : {4, 5}
}

"""
to easily construct such dictionary, you use dafaultdict in the collections module.
a feature of defaultdict is that it automatically initializes the first value so you
can simply focus on adding items.
"""

from collections import defaultdict

d = defaultdict(list)
d['a'].append(1)
d['a'].append(2)
d['b'].append(3)
d['b'].append(4)
d['a'].append(5)
print(f"Default (list) dictionary: {d}\n")

d = defaultdict(set)
d['a'].add(1)
d['a'].add(1)
d['b'].add(3)
d['b'].add(4)
d['a'].add(5)
print(f"Default (set) dictionary: {d}\n")

# using setdefault
d = {} # A regular dictionary
d.setdefault('a', []).append(1)
d.setdefault('a', []).append(2)
d.setdefault('b', []).append(4)
print(f"using setdefault: {d}\n")

# in principle, constructing a multivalued dictionary is simple. However, initialization
# of the first value can be messy if you try to do it yourself.
pairs = [(1, 2), (2, 3), (3, 4), (5, 6)]

d = {}
for key, value in pairs:
    if key not in d:
        d[key] = []
    d[key].append(value)

# using a defaultdict simply leads to much cleaner code
d = defaultdict(list)
for key, value in pairs:
    d[key].append(value)

# ================================================================================
"""
1.7. keeping dictionary in order

Problem: you want to create a dictionary and you also want to control the order
         of items when iterating or serializing.

Solution: To control the order of items in a dictionary, you can use an OrderedDict from the
          collections module.
"""

from collections import OrderedDict

d = OrderedDict()
d['foo'] = 1
d['bar'] = 2
d['jon'] = 3
d['doe'] = 4
print(d)

import json
print(json.dumps(d))
