# String formatting

# Old style string formatting
name = 'Mrinal'
print('Hello %s' % name)

# %x format specifier to convert an int value to a string and
# represent it as a hexidecimal number:
errno = 50159747054
print('%x' % errno)

print('Hey %s, there is 0x%x error!' % (name, errno))
# It's also possible to refer to variable substitutions by name in your format
# string, if you pass a mapping to the %-operator:

print('Hey %(name)s, there is Ox%(errno)s error!' % {"name": name, "errno": errno})
# This makes your format strings easier to maintain and easier to modify in the future.

# New Style string formatting
print('Hello, {}'.format(name))
print('Hey {name}, there is a 0x{errno:x} error!'.format(name=name, errno=errno))

# Literal String Interpolation (Python 3.6+)
print(f'Hello, {name}!')
a = 8; b = 9
print(f'Five plus ten is {a + b} and not {2 * (a + b)}')
print(f'Hey {name}, there is a {errno:#x} error!')
