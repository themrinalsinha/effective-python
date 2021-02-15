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

