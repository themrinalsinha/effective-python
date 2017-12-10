# Item 9 : Consider generator expression for large comprehensions

# List comprehension is fine when there is limited or short values for larger value you should be using generator.
# Generator expression dont materialize the whole output sequence when they're run. Instead generator expression evaluates to an iterator that yield one item at a time from the expression.
# A generator expression is created by putting list-comprehension like syntax between () characters.

# Using List
ls = [len(x) for x in open('test_9.txt')]
print(ls)

# Using Generator
it = (len(x) for x in open('test_9.txt'))
print(it)
print(next(it))
print(it.__next__())

# Another powerful outcome of generator expression is that they can be composed together. Here I take the iterator returned byt the generator expression above and use it as the input for another generator expression.
root = ((x, x ** 0.5) for x in it)
print(next(root))

# Chaining generators like this executes very quickly in python. when you are looking for a way to compose functionality that's operating on a large stream of input. generator expression are the best tool for te job.

# List comprehensions can cause problems for alrge inputs by too much memory.
# Generator expression avoides memory issues by providing output one at a time as an iterator.
# Generator expression can be composed by passing the iterator from one generator expression into the for subexpression of another.
# Generator expression execute very quickly when chained together.
