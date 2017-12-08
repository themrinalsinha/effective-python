# Item 6 : Avoid using start, end and stride in a single slice.

# In addition to Item 5. Python has special syntax for the stride of a slice in the form 
# somelist[start:end:stride]. This lets you take every nth item when slicing a sequence.

a    = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
odds = a[::2]
even = a[1::2]

# The problem is that the stride syntax often causes unexpected behaveior that can introduce bugs.
# strides works well for byte strings and ASCII characters, but it will break for Unicode characters encoded as UTF-8 byte string.

# Are negative strides beside -2 useful
print(a[::2])
print(a[::-2])
print(a[2::2])
print(a[-2::-2])
print(a[-2:2:-2])
print(a[2:2:-2])

