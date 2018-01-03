# Item 21 : Enforce clarity with keyword-only arguments.

# Passing argument by keyword is a powerful feature of Python functions. The flexibility of keyword arguments enables you to write code that will be clear for your use cases.
# Eg. you want to divide one number by another but be very careful about special cases. Sometimes you want to ignore ZeroDivisionError exceptions and return infinity instead. Other times, you want to ignore OverflowError exceptions and return zero instead. 

def safe_division(number, divisor, ignore_overflow, ignore_zero_division):
    try:
        return number / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise
# Using this function is straightforward. This call will ignore the float overflow from divisio and will return zero.
result = safe_division(1, 10**500, True, False)
print(result)

# This call will ignore the error from dividing by zero and will return infinity.
result = safe_division(1, 0, False, True)
print(result)

# The problem is that it's easy to confuse the position of the two Boolean arguments that control the exception-ignoring behavior. This can easily cause bugs that are hard to track down. On way to improve the readability of this code is to use keyword argument.
# eg:
def safe_division1(number, divisor, ignore_overflow=False, ignore_zero_division=False):
    try:
        return number / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise
# Then callers can use keyword arguments to specify which of the ignore flags they want to flip for specific operations, overriding the default behavior.
print(safe_division1(1, 10**500, ignore_overflow=True))
print(safe_division1(1, 0, ignore_zero_division=True))
# You can still call it the old way with positional arguments, which is a problem.
print(safe_division1(1, 10**500, True, False))

# With the complex functions like this, it's better to require that callers are clear about their intentions. In Python3, you can demand clarity by defining your functions with keyword-only arguments. These arguments can only be supplied by keywod, never by position.
# Here, I redefine the safe_division function to accept keyword-only arguments. The * symbol in the argument list indicates the end of positional arguments and the beginning of keyword-only arguments. 

# Accept Keyword-only arguents.
def safe_division2(number, divisor, *, ignore_overflow=False, ignore_zero_division=False):
    try:
        return number / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise
print(safe_division2(1, 10**500, ignore_overflow=True))
print(safe_division2(1, 0, ignore_zero_division=True))
# print(safe_division2(1, 10**500, True, False)) # It won't work, this time.

# NOTE:
# -> Keyword arguments make the intention of a function call more clear.
# -> Use keyword-only arguments to force callers to supply keyword arguments for potentially confusiong functions, especially those thta accept multiple boolean flags. 

# ==================================================================================================

# Keyword-Only Augument in python2
# -> Python2 doesn't have explicit syntax for specifying keyword-only arguments like Python3.
# But you can achieve the same behavior of raising TypeErrors for invalid function calls by using the ** operator in argument lists. 

def print_args(*args, **kwargs):
    print('Positional Arguments : ', args)
    print('Keyword Arguments    : ', kwargs)
print_args(1, 2, 3, 4, tms='Mrinal Sinha', warlock='Lucky Singh')

