"""
1.4. finding the largest or smallest N items

Problem: you want to make a list of the largest or smallest N items in a collection

Solution: the heapq module has two functions - nlargest() and nsmallest() -- that do exactly what we want.
"""

from heapq import nlargest, nsmallest, heapify

nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
print(f"largest 3 numbers: {nlargest(3, nums)}")
print(f"smallest 3 numbers: {nsmallest(3, nums)}\n")

portfolio = [
    {'name': 'IBM', 'shares': 100, 'price': 91.1},
    {'name': 'AAPL', 'shares': 50, 'price': 543.22},
    {'name': 'FB', 'shares': 200, 'price': 21.09},
    {'name': 'HPQ', 'shares': 35, 'price': 31.75},
    {'name': 'YHOO', 'shares': 45, 'price': 16.35},
    {'name': 'ACME', 'shares': 75, 'price': 115.65}
]

cheap = nsmallest(3, portfolio, key=lambda s: s['price'])
expen = nlargest(3, portfolio, key=lambda s: s['price'])
print(f"Cheapest (3): {cheap}")
print(f"Expensive (3): {expen}\n")

"""
if you are looking for the N smallest or largest items and N is small compared to the
overall size of the collection, these functions provide superior performance.
"""
original = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
heap = list(original)
heapify(heap)
print(f"{original} --> heapify --> {heap}")
