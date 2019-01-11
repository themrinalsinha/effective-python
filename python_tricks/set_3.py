# Functions are objects
def yell(text):
    return text.upper() + '!'
bark = yell
del yell
# You can delete the function's original name (yell).
# Since another name bark still points to the underlying function
print(bark('Hello'))

# Python attaches a string identifier to every function at creation time for
# debugging purposes. You can access the internal identifier with the __name__ attributes
print(bark.__name__)
# Now you can see even after deleting yell here the above statement prints yell.
# This doesn't affect how you can access the function object from your code.

# FUnctions can be stored in data structures
# Functions can be passed to another functions.

# The classic example to high order function in python is the built-in map function.
print(list(map(bark, ['Hello', 'Mrinal', 'Sinha'])))
# As you saw, map went through the entire list an applied the bark funciton to each element.
# As a result, we now have a list object with modified greeting strings...


# Functions can access the text parameter defined in parent function. In fact, they seems to capture
# and remember the value of that argument. Functions that do this are called lexical closure (or just closure)
def make_adder(n):
    def add(x):
        return x + n
    return add

plus_3 = make_adder(5)
print(plus_3(3))
# Here make_adder serves as a factory to craete and configure "adder" functions.
