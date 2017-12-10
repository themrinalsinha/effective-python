# Item 11 : Use zip to process iterators in parallel

# List comprehensions make it easy to take a source list and get a derived list by applying an expression.

names   = ['Mrinal', 'Kunal', 'Rishab', 'Nirbhey']
letters = [len(n) for n in names]

print(names)
print(letters)

# the items in the derived list are related to the items in the source list by their indexes. To iterate over both lists in parallel, you can iterate over the lenght of the names source list.
longest_name = None
max_letters  = 0

for i in range(len(names)):
    count = letters[i]
    if count > max_letters:
        longest_name = names[i]
        max_letters  = count
print(longest_name)
# The problem in this whole loop statement is visually noisy. The indexes into names an letters make it hard to read.

# Slight improvement, usign enumerate.
for i, name in enumerate(names):
    count = letters[i]
    if count > max_letters:
        longest_name = name
        max_letters  = count
print(longest_name)

# To make the above code clearer python provides the zip built-in function. 
# zip wraps two or more iterator with a lazy generator. The list generator yields tuples containing the next value from each iterator.
for name, count in zip(names, letters):
    if count > max_letters:
        longest_name = name
        max_letters  = count
print(longest_name)

# Can also make dictonary:
names = dict(zip(names, letters))
print(names)