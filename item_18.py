# Item 18 : Reduce Visual Noise with Variable Positional Arguments.

# Accepting optional positional arguments (often call star args in reference to the conventional name for the parameter, *args) can make a function call more clear and remove visual noise.
# Eg: Say you want to log some debug information. With a fixed number of arguments, you would need a function that takes a message and a list of values.

def log(message, values):
    if not values:
        print(message)
    else:
        values_str = ', '.join(str(x) for x in values)
        print('%s : %s' % (message, values))

log('My numbers are', [1,2,3,4])
log('Hello world..', [])

# Having to pass an empty list when you have no values to log is cumbersome and noisy, It'd be better to leave out the second argument parameter name with *. The first parameter for the log message is required, whereas any number of subsequent positional arguments are optional. The function body doesn't need to change, only the caller do.
def log(message, *values):
    if not values:
        print(message)
    else:
        values_str = ', '.join(str(x) for x in values)
        print('%s : %s' % (message, values))

log('My numbers are', 1,2,3,4)
log('Hello world..')

# The variable arguments are always turned into a tuple before they are passed to your function. This means that if the caller of your funciton uses the * operator on a generator, it will be iterated until it's exhausted. The resulting tuple will include every value from the generator, which could consume a lot of memory and cause your program to crash.
def my_generator():
    for i in range(10):
        yield i

def my_func(*args):
    print(args)

it = my_generator()
my_func(*it)

# The second issue with *args is that you can't add new positional arguments to your function in the future without migrating every caller. If you try to add a positional argument in the front of the argument list, existing callers will subtly break if they aren't updated.

def log(sequence, message, *values):
    if not values:
        print('%s : %s' % (sequence, message))
    else:
        values_str = ', '.join(str(x) for x in values)
        print('%s : %s :%s' % (sequence, message, values_str))
log(1, 'Favorites', 7, 33)
log('Favriot number', 7, 33)

# Notes:
# -> Functions can accept a variable number of positional argument by using *args in the def statement
# -> You can use the items from a sequence as the positional arguments for a function with the * operator.
# -> Using the * operator with a generator may cause your program to run out of memory and crash.
# -> adding new positional parameters to functions that accepts *args can introduce hard-to-find bugs. 