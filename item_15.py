# Item - 15 : Know how closure interact with variable scope

# you want to sort a list of numbers but prioritize one group of numbers to come first. This pattern is useful when you're rendering a user interface and want important messages or exceptional events to be displayed before everything else.abs

# A common way to do this is to pass a helper function as the key argument to a list's sort method. The helper's return value will be used as the value for sorting each item in the lsit. The helper can check whether the given item is in the important group and can vary the sort key accordingly.

def sort_priority(values, group):
    def helper(x):
        if x in group:
            return (0, x)
        return (1, x)
    values.sort(key = helper)

numbers = [8, 3, 1, 2, 8, 9, 0, 6, 5]
group   = {2, 9, 5, 3}
sort_priority(numbers, group)
print(numbers)
# There are three reasons why this function operates as expected:
# -> Python supports closure : functions that refer to variables from the scope in which they were defined. This is why the helper function is able to access the group argument to sort_priority.
# -> Functions are first-class objects in python, meaning you can refer to them directly, assign them to variable, pass them as arguments to toher functions, compare them in expressions and if sttements, etc. This is how the sort method can accept a closure function as the key argument.
# -> Python has specific rules for comparing tuples. It first compares items in index zero, then index one, then index two, and so on,.. This is why the return value from the helper closure cause the sort order to have two distinct groups.

# It'd be nice if this function returned whether higher-priority items were seen at all so the user interface code can act accordingly. Adding such behavior seems straightforward. There's already a closure function for deciding which group each number is in. Why not also  use the closure to flip a flag when high-priority items are seen ? Then the function  can return the flag value after it's been modified by the closure.

def sort_priority2(numbers, group):
    found = False
    def helper(x):
        if x in group:
            found = True
            return (0, x)
        return (1, x)
    numbers.sort(key = helper)
    return found

numbers = [8, 3, 1, 2, 8, 9, 0, 6, 5]
group   = {2, 9, 5, 3}
found = sort_priority2(numbers, group)
print(found)
print(numbers)

# NOTE:
# -> Closure functions can refer to variables from any of the scopes in which they were defines.
# -> By default, closures can't affect enclosing scopes by assigning variables.
# -> In python3,  use the nonlocal statement to indicate when a closure can modify a variable in its enclosing scopes. 