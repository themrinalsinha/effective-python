# Lamdbas are single expression functions
# The lambda keyword in python provides a shortcut for declaring small anonymous functions. They behave just like regular FUnctions
# eg:
temp = '\n{}\n'.format('-'*40)

add = lambda x, y: x + y
print('Addition: ', add(2, 3), end=temp)

# Another way of doing it...
res = (lambda x, y: x - y)(19, 6)
print('Called inline lambda function and called it immediately..')
print('Subtraction (single line): ', res, end=temp)

# Lamdbas you can use.
tuples = [(1, 'd'), (2, 'b'), (5, 'c'), (3, 'a'), (4, 'e')]
print('Before sorting: ', tuples)
x  = sorted(tuples, key=lambda x: x[0])
xx = sorted(tuples, key=lambda x: (x[1], x[0]))
print('After sorting:', x)
print('Multikey sort:', xx, end=temp)

xxx = sorted(range(-5, 5), key=lambda x: x * x)
print(xxx, end=temp)

# Lexical closure!
# It is refered to function that remembers the values from the enclosing Lexical
# scope even when the program flow in no longer in that scope even when the program
# flow in no longer in that scope.
def make_adder(n):
    return lambda x: x + n

plus_3 = make_adder(4)
print(plus_3)
print(plus_3(3), end=temp)
