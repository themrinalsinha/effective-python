"""
7.12. accessing variables defined inside a closure

Problem: you would like to extend a closure with functions that allows the inner variable
         to be accessed and modified.

Solution: Normally, the inner variable of a closure are completely hidden to the outside
          world. However, you can provide access by writing accessor function and attaching
          them to the closure as function attributes.
"""

def sample():
    n = 0

    # closure function
    def func():
        print('n=', n)

    # accessor method for n
    def get_n():
        return n

    def set_n(value):
        nonlocal n
        n = value

    func.get_n = get_n
    func.set_n = set_n
    return func

# example of using the above code
f = sample()
f()

f.set_n(10)
f()

f.get_n()

# There are two main features that make this recipe work. First, nonlocal declarations
# make it possible to write functions that change inner variables. Second, function at‐
# tributes allow the accessor methods to be attached to the closure function in a straight‐
# forward manner where they work a lot like instance methods (even though no class is
# involved).
