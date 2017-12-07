# Item 5 : Know how to slice sequences

# Slicing lets you access a subset of a sequence's items with minimal effort.
# The simplest uses for slicing are in the built-in types list, str, and bytes. 
# Slicing can be extended to any Python class that implemets the __getitem__ and __setitem__ special methods

# Basic form somelist[start:end], where start -> inclusive and end -> exclusive.

a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
print(a[:4]) #First four
print(a[-4:]) #Last four
print(a[3:-3]) #Middle two