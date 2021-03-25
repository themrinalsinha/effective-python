"""
Item 4: Prefer Interpolated F-Strings over C-style format strings and str.format
"""

a = 0b10111011
b = 0xc5f
print('Binary is %d, hex is %d' % (a, b))

k = 'my_var'
v = 1.2345

formatted = '%-10s = %.2f' % (k, v)
print(formatted)

# But if you swap k and v, you get an exceptional at runtime
# reordered_tuple = '%-10s = %.2f' % (v, k)
# print(reordered_tuple)
# TypeError: must be real number, not str

pantry = [
    ('avocados', 1.25),
    ('bananas', 2.5),
    ('cherries', 15),
]

for i, (item, count) in enumerate(pantry):
    print('# %d: %-10s = %.2f' % (i, item, count))

k = 'my_var'
v = 1.23456

# old_way = '%-10 = %.2f' % (k, v)
# new_way = '%(k)-10s = %(v).2f' % {'k': k, 'v': v} # original
# rec_way = '%(k)-10s = %(v).2f' % {'v': v, 'k': k} # swapped

# assert old_way == new_way == rec_way
# -------------------------------------------------------------

# Interpolated Format Strings
key = 'may_var'
val = 1.2345678

formatted = f'{key} = {val}'
print(formatted)

formatted = f'{key!r:<10} = {val:.2f}'
print(formatted)
