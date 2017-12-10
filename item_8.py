# Item 8 : Avoide more than two expression in list comprehension

# List comprehensions also support multiple levels of looping. 

matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

# It is simple, readable and a reasonable usage of multile loop.
flat   = [x for row in matrix for x in row]
print(flat)

# Now you want to square the value in each cell of a two-dimensional matrix. This expression is noisier because of the extra[] charactersbut it's still easy to read.
squared = [[x**2 for x in row] for row in matrix]
print(squared)

# If this expression included another loop, the list comprehension would get so long that you'd get so long that you'd have to split it over multiple lines.
my_list   = [[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]]
flat_list = [x for sub_list_1 in my_list for sub_list_2 in sub_list_1 for x in sub_list_2]
print(flat_list)
# OR
flat_list = []
for sub_list_1 in my_list:
    for sub_list_2 in sub_list_1:
        flat_list.extend(sub_list_2)
print(flat_list)

# List comprehensions also support multiple if conditions. Multiple conditions at the same loop level are implicit and expression.
# If you want to filter a list of numbers to only even values greater than four. These two list comprehension are equivalent.
a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

b = [x for x in a if x > 4 if x % 2 == 0]
print(b)

c = [x for x in a if x > 4 and x % 2 == 0]
print(c)

# Conditions can be specified at each level of looping after the for expression.
# Say you want to filter a matrix so the only cells remaining are those divisible by 3 in rows that sum to 10 or higher. Expressing this with the list comprehension is short, but extremely difficult to read.

matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
filter = [[x for x in row if x % 3 == 0] for row in matrix if sum(row) > 10]
print(filter)

# List comprehensions support multiple level of loops and multiple conditions per loop levels.
# List comprehensions with more than two level should be avoided.