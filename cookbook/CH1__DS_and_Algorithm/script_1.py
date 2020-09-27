"""
1.1. unpacking a sequence into separate variables

Problem: you have an N-element tuple or sequence that you would like to unpack
         into a collection of N vairables.
"""

p = (4, 5)
x, y = p
print(f"({x}, {y})")

data = ['ACME', 50, 91.1, (2012, 12, 21)]
name, shares, price, date = data

# NOTE: if there is mismatch in the number of elements, you'll get an error
# eg: p = (4, 5) | x, y, z = p it will throw ValueError
# ================================================================================

"""
1.2. unpacking elements from iterables of arbitrary length

Problem: you need to unpack N elements from an iterable, but the iterable may be longer
         than N elements, causing a "too many values to unpack" exception.

Solution: "star expression" can be used to address this problem
"""

record = ('Dave', 'dave@example.com', '773-555-1212', '847-555-1212')
name, email, *number = record
print(f"\nName: {name}\nEmail: {email}\nContact: {number}")

*trailing, current = [10, 8, 7, 1, 9, 5, 10, 3]
print(f"\nTrailing: {trailing}\nCurrent: {current}")

line = 'nobody:*:-2:-2:Unprivileged User:/var/empty:/usr/bin/false'
uname, *fields, homedir, sh = line.split(':')

# sometimes you might want to unpack values and throw them away. you can just
# specify a bare * when unpacking, but you could use a common throwaway variable name,
# such as _ or ign(ignore)
record = ('ACME', 50, 123.45, (12, 18, 2012))
name, *_, (*_, year) = record
print(f"\nName: {name}\nYear: {year}")
