"""
item 58: profile before optimizing

the dynamic nature of python causes surprising behaviors in its runtime performance.
operations you might assume are slow are actually very fast (string manipulation, generators).
The true source of python source slowdowns in python program can be obscure.

The best approach is to ignore the intuition and directly measure the performance of a program
before you try to optimize it. Python provides a built-in profiler for determining which parts
of a program are responsible for its execution time. This let's you focus on your optimization
efforts on the biggest source.
"""

def insertion_sort(data):
    result = []
    for value in data:
        insert_value(result, value)
    return result

def insert_value(array, value):
    for i, existing in enumerate(array):
        if existing > value:
            array.insert(i, value)
            return
    array.append(value)

"""
To profile insertion sort and insert_value, We'll crate a dataset of random numbers and
define a rest function to the pass to the profiler.
"""

from random import randint

max_size = 10 ** 4
data = [randint(0, max_size) for _ in range(max_size)]
test = lambda: insertion_sort(data)

"""
Python provides two built-in profilers, on that is pure Python (profiler) and another one is C-extension
module (cProfile). The cProfile built-in module is better because of it's minimal impact on the performance
of your program while it's being profiled. The pure python alternative imposes a high overhead that will
skew that results.
"""

from cProfile import Profile

# running profiling
profile = Profile()
profile.runcall(test)

"""
Once the test function has finished running, I can extract statistics about its performance using the pstats
built-in module and its Stats class. Various methods on a Stats object adjust how to select and sort the
profiling information to show only the things you care about.
"""
from pstats import Stats

stats = Stats(profile)
stats.strip_dirs()
stats.sort_stats('cumulative')
stats.print_stats()
