"""
1.11. Naming a slice

Problem: your program has become an unreadable mess of hardcoded slice indices and
         you want to clean it up..
"""

record = '0123456789012345678901234567890123456789012345678901234567890'
cost   = int(record[20:32]) * float(record[40:48])
print(f'COST: {cost}')

SHARES = slice(20, 32)
PRICE = slice(40, 48)
cost = int(record[SHARES]) * float(record[PRICE])
print(f'COST: {cost}')

# you avoid having a lot of mysterious hardcoded indices, and what you're doing
# becomes much clearer.

items = [0, 1, 2, 3, 4, 5, 6]
a = slice(2, 4)
print(items[2:4]) # or
print(items[a])

items[a] = [100, 200]
print(items)

del items[a]
print(items)

# if you have a slice instance s, you can get more information about it by looking
# at its s.start, s.stop and s.step attribute, respectively, eg:
a = slice(10, 50, 2)
print(f"\nSLICE object\nstart: {a.start}\nstop: {a.stop}\nstep: {a.step}")

# you can map a slice onto a sequence of specific size by using its indices(size) method.
# this returns a tuple (start, stop, step) where all values have been suitably limited to
# fit within bounds (as to avoide IndexError exception when indexing)

s = 'Hello World'
print(a.indices(len(s)))

for i in range(*a.indices(len(s))):
    print(s[i])


