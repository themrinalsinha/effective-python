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
# Applying multiple decorator to a function.
def strong(func):
    def wrapper():
        return '<strong>' + func() + '</strong>'
    return wrapper

def emphasis(func):
    def wrapper():
        return '<em>' + func() + '</em>'
    return wrapper

@uppercase
@strong
@emphasis
def greet():
    return 'Hello there...'

print(greet())
# Note: decorators are applied from bottom to top
# --------------------------------------------------------------

# Decorating function that takes arguments.
def proxy(func):
    def wrapper(*args, **kwargs):
        print(f'TRACE: calling {func.__name__}() with {args} and {kwargs}')
        original_result = func(*args, **kwargs)
        return func(*args, **kwargs)
        print(f'Returned original {func.__name__}()')
    return wrapper

@proxy
def say(name, line):
    return f'{name} : {line}'

print(say('Mrinal', 'Welcome onboard!'))
