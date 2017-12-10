# Item 7 : Use List Comprehensions Instead of map and filter

# Python provides compact syntax for deriving one list from another. These expression are called list comprehensions.

a            = [1, 2, 3, 4, 5, 6, 7, 8, 9]
squares_list = [x**2 for x in a]
print(squares_list)

# map requires creating a lambda function which is visually noisy.
squares_map  = map(lambda x : x ** 2, a)
print(list(squares_map))

# We can add conditional expression to the list comprehension after the loop.
squares_even = [x**2 for x in a if x % 2 == 0]
print(squares_even)

# the filter built-in function can be used along with map to achieve the same outcome, but it is much harder to read.
square_filter = map(lambda x : x ** 2, filter(lambda x : x % 2 == 0, a))
print(list(square_filter))

# Dictonaries and sets have their own equivalents of list comprehensions. This make it easy to create derivative data structures when writing algorithms.
name_ranks = { 'Mrinal' : 1, 'Kunal' : 2, 'Rishab' : 3, 'Nirbhey' : 4 }
print(name_ranks)

ranks = {rank:name for name, rank in name_ranks.items()}
print(ranks)