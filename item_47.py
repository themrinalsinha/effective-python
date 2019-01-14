# Use decimal when precision is paramount.

# Python is an excellent language for writing code that interacts with numerical data.
# Python's integer type can represent values of any practical size. It doubles-precision
# floating point type compiles with the IEEE 754 standard. The language also provides
# a standard complex number type for imaginary values.

rate = 1.45
# duration 3 min 42 second
seconds = 3 * 60 + 42
cost = rate * seconds / 60
print('COST', cost)
print('ROUNDED', round(cost, 2))

# say now you want to support very short phone calls between places that are much cheaper to connect. Here I copmuter the charge for a phone call that was 5 secondlong with a rate of $0.05/min
rate = 0.05
seconds = 5
cost = rate * seconds / 60
print('COST', cost)
print('ROUNDED', round(cost, 2))
# THis won't work.

# The solution is to use the Decimal class from the decimal built-in module. The decial class provides fixed point math of 28 decimal
# points by default. It can go even heigher if required. This works around the precision issues in IEEE 754 floating point numbers. The
# class also gives you more control over rounding behaviour.

from decimal import Decimal, ROUND_UP

rate = Decimal('1.45')
seconds = Decimal('222') # 3*60 + 42
cost = rate * seconds / Decimal('60')
print('USING DECIMAL CLASS', cost)

# or

rate = Decimal('0.05')
seconds = Decimal('5') # 3*60 + 42
cost = rate * seconds / Decimal('60')
print('USING DECIMAL CLASS (less)', cost)
# but the quantize behavior ensures that this is rounded up to one whole cent.
rounded = cost.quantize(Decimal('0.01'), rounding=ROUND_UP)
print(rounded)

# while Decimal works great for fixed point numbers. It still has limitations in its precision.
# for representation rational numbers with no limit to precision. consider using the fraction from the fractions built-in module.
