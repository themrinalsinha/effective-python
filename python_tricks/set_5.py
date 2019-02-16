# A decorator is a callable that takes a callable as input and returns another callable.

# Eg:
def null_decorator(func):
    return func

# null_decorator is a callable (function), it takes another callable as its input, and it
# returns the same input callable without modifying it.

@null_decorator
def greet():
    return 'Hello'

# greet = null_decorator(greet)
# print(greet()) ### or
# -------------------------------------------------------------

# A slightly more complex decorator which converts the result of the decorated
# function to uppercase letter.

def uppercase(func):
    def wrapper():
        original_result = func()
        modified_result = original_result.upper()
        return modified_result
    return wrapper

@uppercase
def greet():
    return 'Hello there, how are you ??'

print(greet())
# --------------------------------------------------------------
