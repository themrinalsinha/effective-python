# Item 42: Define Function Decorators with 'functools.wraps'

# Decorators have the ability to run additional code before and after any calls to the functions they wrap.
# This allows them to access and modify input arguments and return values. This functionality can be useful
# for enforcing semantics, debugging, registering functions and more..
#
# Eg. say you want to print the arguments and return value of a function call. This is especially helpful when
# debugginga stack of function calls from a recursive function. Here, I define such a decorator:

def trace(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print('%s (%r, %r) -> %r' % (func.__name__, args, kwargs, result))
        return result
    return wrapper

# I can apply this to a function using the @ symbol

@trace
def fibonacci(n):
    """Return the n-th Fibonacci number"""
    if n in (0, 1):
        return n
    return (fibonacci(n-2) + fibonacci(n-1))

# The @ symbol is equivalent to calling the decorator on the function it wraps and assigning the return value to the original name in the same scope.

fibonacci = trace(fibonacci)
# Calling this decorator function will run the wrapper code before and after fiboacci runs, printing the arguments and return value at each level in the recursive stack.

fibonacci(3)
# This works well, but it has an uninteended side effect. The value returned by the decorator-the function that's called above doesn't think it's name fibonacci.
print(fibonacci)

# The trace function returns the wrapper it defines. The wrapper function is what's assigned to the fibonacci name in the containing module because of the decorator.
# The behavior is problamatic because it undermines tools thta do introspection, such as debugger and objecg serializer
# for example, the help built-in function is useless on the decorated fibonacci function.
# print(help(fibonacci))

# The solution is to use th wraps helper function from the functools built-in module. This is a decorator that helps you write decorators.
# Applying it to the wrapper functino will copy all of the important meta-data about the inner function to the outer function.

from functools import wraps

def trace_smart(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print('%s (%r, %r) -> %r' % (func.__name__, args, kwargs, result))
        return result
    return wrapper

@trace_smart
def fibonacci_smart(n):
    """Return the n-th Fibonacci number"""
    if n in (0, 1):
        return n
    return (fibonacci(n-2) + fibonacci(n-1))

fibonacci_smart = trace_smart(fibonacci_smart)
fibonacci_smart(5)
print(fibonacci_smart)
# print(help(fibonacci_smart(5)))

# Now, running the help function produces the expected result, even though the function is decorated.

# Things to remember:
# -> Decorator are python syntax for allowing one function to modify another function at runtime.
# -> Using decorator can cause strange behaviors in tools that do introspection, succh as debugger.
# -> Use the wraps decorator from the functools built-in module when you define your own decorators to avoid any issues.
