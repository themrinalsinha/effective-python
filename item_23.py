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

# Supplying functions like log_missing makes APIs easy to build and test because it seperates side effects from deterministic behavior.
# eg: say you now want the default value hook passed to defaultdict to count the total number of keys that were missing.
# One way to achieve this is using astateful closure
# Here I define a helper function that uses such a closure as the default value hook:

def increment_with_report(current, increment):
    added_count = 0

    def missing():
        nonlocal added_count #Stateful closure
        added_count += 1
        return 0

    result = defaultdict(missing, current)
    for key, amount in increments:
        result[key] += amount
    
    return result, added_count

# Running the function produces the expected result(2), even though the defaultdict has no idea that the missing hook maintains state.
# This is another benefit of accepting simple functions for interfaces. It's easy to add functionality later by hiding state in a closure.