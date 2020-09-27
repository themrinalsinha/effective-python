"""
1.8. calculating with dictionaries

Problem: you want to perform various calculations (eg: min value, max value sorting etc)
"""
prices = {
    'ACME': 45.23,
    'AAPL': 612.78,
    'IBM': 205.55,
    'HPQ': 37.20,
    'FB': 10.75
}

min_price = min(zip(prices.values(), prices.keys()))
print(f"Minimum price: {min_price}")

max_price = max(zip(prices.values(), prices.keys()))
print(f"Maximum price: {max_price}")

prices_sorted = sorted(zip(prices.values(), prices.keys()))
print(f"Sorted: {prices_sorted}")

# another way to do this
min_price = min(prices, key=lambda x: prices[x])
max_price = max(prices, key=lambda x: prices[x])
print(f"\nMin: {min_price}\nMax: {max_price}\n\n")
# ==========================================================================================

"""
1.9. finding commonalities in two dictionaries

Problem: you have two dictionaries and want to find out what they might have in common (same key, same value etc)
"""
a = {
    'x': 1,
    'y': 2,
    'z': 3
}

b = {
    'w': 10,
    'x': 11,
    'y': 2
}

# IMPORTANT:
# To find our what the two dictionaries have in common, simply perform common set
# operations using the keys() or items() methods, eg:
print(f"common keys: {a.keys() & b.keys()}")
print(f"key in 'a' that are not in 'b': {a.keys() - b.keys()}")
print(f"key in 'b' that are not in 'a': {b.keys() - a.keys()}")
print(f"(key, value) pair in common: {a.items() & b.items()}")

# These kinds of operations can also be used to alter or filter dictionary contents. For
# example, suppose you want to make a new dictionary with selected keys removed. Here
# is some sample code using a dictionary comprehension:

# make a new dictionary with certain keys removed
c = {key: a[key] for key in a.keys() - {'z', 'w'}}
print(c)
