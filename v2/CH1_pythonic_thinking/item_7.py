"""
Item 7: Prefer enumerate over range

The range built-in function is useful for loops that iterate over a set of integers
"""

from random import randint

random_bits = 0

for i in range(32):
    if randint(0, 1):
        random_bits |= 1 << i

print(random_bits)
print(bin(random_bits))

flavor_list = ['vanilla', 'chocolate', 'pecan', 'strawberry']
for i, flavor in enumerate(flavor_list):
    print(i, flavor)

for i, flavor in enumerate(flavor_list, start=1):
    print(i, flavor)
