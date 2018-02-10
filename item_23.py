# Accept functions for Simple Interfaces Instead of Classes

# Many of python's built-in APIs allow you to customize behavior by passing in a function. These hooks are used by APIs to call back your code while they execute.
# eg: the list type's sort method takes an optional key argument that's used to determine each index's value for sorting.
# Here, I sort a list of names based on their lengths by providing a lambda expression as the key hook:

names = ['Socrates', 'Archimedes', 'Plato', 'Aristotle']
names.sort(key = lambda x : len(x))
print(names)

# Eg: say you want to customize the behavior of the defaultdict class. The data structure allows yo uto supply a function that will be caled each time a missing key is accessed.
# The function must return the default value the missing key is accessed. The function must return the default value the missing key should have in the dictionary.
# Here I define a hook that logs each time a key is missing and returns 0 for the default value:
from collections import defaultdict

def log_missing():
    print('Key added')
    return 0

current    = {'green' : 12, 'blue' : 3}
increments = [
    ('red', 5),
    ('blue', 17),
    ('orange', 9),
]

result = defaultdict(log_missing, current)
print('Before : ', dict(result))
for key, amount in increments:
    result[key] += amount
print('After : ', dict(result))