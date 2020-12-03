"""
9.16. Enforcing an argument signature on *args and **kwargs

Problem: You've written a function or method that uses *args and **kwargs, so that it
         can be general purpose, but you would also like to check the passed arguments
         to see if they match a specific function calling signature.

Solution: For any problem where you want to manipulate function calling signatures, you
          should use the signature features found in the inspect module. Two classes
          Signature and Parameter, are of particular interest here. Here is an interactive
          example of creating a function signature.
"""

from inspect import Signature, Parameter

# make a signature for a func(x, y=42, *, z=None)
params = [ Parameter('x', Parameter.POSITIONAL_OR_KEYWORD),
           Parameter('y', Parameter.POSITIONAL_OR_KEYWORD, default=42),
           Parameter('z', Parameter.KEYWORD_ONLY, default=None) ]

signature = Signature(params)
print(f"Function signature: {signature}")

# once you have a signature object, you can easily bind it to *args and **kwargs using
# the signature's bind() method, as shown in this simple example:
def func(*args, **kwargs):
    bound_values = signature.bind(*args, **kwargs)
    for name, value in bound_values.arguments.items():
        print(name, value)

func(1, 2, z=3)
func(1)
func(1, z=3)
func(y=2, x=1)
# func(1, 2, 3, 4) # will throw error.

# As you can see, the binding of a signature to the passed arguments enforces all of
# the usual function calling rules concerning required arguments, defaults, duplicates
# and so forth.

from inspect import Signature, Parameter

def make_sig(*names):
    params = [ Parameter(name, Parameter.POSITIONAL_OR_KEYWORD) for name in names ]
    return Signature(params)

class Structure:
    __signature__ = make_sig()

    def __init__(self, *args, **kwargs) -> None:
        bound_values = self.__signature__.bind(*args, **kwargs)
        for name, value in bound_values.arguments.items():
            setattr(self, name, value)

class Stock(Structure):
    __signature__ = make_sig('name', 'shares', 'price')

class Point(Structure):
    __signature__ = make_sig('x', 'y')

# Here is an example of how the Stock class works
import inspect
print(inspect.signature(Stock))

s1 = Stock("ACME", 100, 490.1)
# s2 = Stock("ACME", 100) # will throw error coz price is missing

# The use of functions involving *args and **kwargs is very common when trying to
# make general-purpose libraries, write decorators or implement proxies. However, one
# downside of such functions is that if you want to implement your own argument check‐
# ing, it can quickly become an unwieldy mess
