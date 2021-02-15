"""
3.1. Rounding Numerical Values

Problem: You want to round a floating-point number to a fixed number
         of decimal places.

Solution: For simple rounding, use the built-in round(value, ndigits) functions.
"""
print(round(1.23, 1))
print(round(1.27, 1))
print(round(-1.27, 1))
print(round(1.25361, 3))

a = 1627731
print(round(a, -1))
print(round(a, -2))
print(round(a, -3))
print()

x = 1.23456
print(f"{x:0.2f}")
print(f"{x:0.3f}")

a = 2.1
b = 4.2
c = a + b
print(c)
print(f"{round(c, 2)}")
# -------------------------------------------------------------------------------

"""
3.2. Performing accurate decimal calculations

Problem: You need to perform accurate calculations with decimal numbers, and don't
         want the small errors that naturally occur with floats.

Solution: A well-known issue with floating-point numbers is that they can't accurately
          represent all base-10 decimals. Moreover, even simple mathematical calculations
          introduce small error.
"""
a = 4.2
b = 2.1
c = a + b
print(c)
print((a + b) == 6.3)

# These errors are a "feature" of the underlying CPU and IEEE 754 arithmetic performed
# by its floating-point units.

from decimal import Decimal
a = Decimal('4.2')
b = Decimal('2.1')
c = a + b
print(c)
print((a + b) == Decimal('6.3'))
# --------------------------------------------------------------------------------

