# Item 17 : Be defensive when iterating over Arguments.

# When a function takes a list of objects as a parameter, it's often important to iterate over that list multiple times.
# Eg: You want to analyze tourism numbers for the US state fo texas. Imagine the data set is the number of visitors to each city (in millions per year). You'd like to fig out what percentage of overall tourism each city recieves.
# To do this you need normalization function. It sums the input to determine the total number of tourist per year.

def normalize(numbers):
    total  = sum(numbers)
    result = []
    for value in numbers:
        percentage = 100 * value / total
        result.append(percentage)
    return result

visits      = [15, 35, 80]
percentages = normalize(visits)
print(percentages)

# To scale this up i need to read the data from a file that contains every city in all of Texas. I define a generator to do this because then I can reuse the same function later when I want to compute tourism numbers for the whole world, a much large data set
def read_visits(data_path):
    with open(data_path) as f:
        for line in f:
            yield int(line)
# Surprisingly, calling normalize on the generator's return value produces no results.
it = read_visits('/tmp/my_numbers.txt')
percentages = normalize(it)
print(percentages)
# output = []

# This cause of this behaviour is that an iterator only produces its results a single time. If you iterate over an iterator or generator that has already raised a StopIteration exception, you won't get any results the second time around.
# what's confusing is that you also won't get any errors when you iterate over an already exhausted iterator.
it = read_visits('/tmp/my_numbers.txt')
print(list(it)) # [12, 54, 23]
print(list(it)) # []

# IMP: To use normalize_func, you can pass in a lambda function that calls the generator and produces a new iterator each time.
percentages = normalize_func(lambda : read_visits(path))

# though it works, having to pass a lambda function like this is clumsy. 
# The better way to achieve the same result is to provide a new container class 
# that implements the iterator protocol.
# The iterator protocol is how python for loops and related expression traverse the contents of a container type.
# When python sees a statement like for x in foo. it will actually call iter(foo). The iter built-in functions calls the foo.__iter__ special method in turn.
# The __iter__ method must return an iterator objects (which itself implements the __next__ special method.)
# Then the for loop repeatedly calls the next built-in functionon the iterator object until it's exhausted.

class ReadVisits(object):
    def __init__(self, data_path):
        self.data_path = data_path
    
    def __iter__(self):
        with open(self.data_path) as f:
            for line in f:
                yield int(line)
# This new container type works correctly when passed to the original function without any modifications.
visits = ReadVisits(path)
percentages = normalize(visits)
print(percentages)

# This works because the sum method in normalize will call ReadVisits.__iter__ to allocate a new iterator objects. The for loop to normalize the numbers will also call __iter_ to allocate a second iterator ojects.
# Each of those iterators will be advanced an dexhausted independently, ensuring that each unique iteration sees all of the input dta values. The only downside of this approach is that it reads the input data multiple times.


