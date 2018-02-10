# Accept functions for Simple Interfaces Instead of Classes

# Many of python's built-in APIs allow you to customize behavior by passing in a function. These hooks are used by APIs to call back your code while they execute.
# eg: the list type's sort method takes an optional key argument that's used to determine each index's value for sorting.
# Here, I sort a list of names based on their lengths by providing a lambda expression as the key hook:

names = ['Socrates', 'Archimedes', 'Plato', 'Aristotle']
names.sort(key = lambda x : len(x))
print(names)

