# Item 41: Consider concurrent.futures for True parallelism.

# The multiprocessing built-in module, easily accessed via. the concurrent.futures built-in module, may be exactly what you need.
# It allows python to utilize multiple CPU cores in parallel by running additional interpreters as child processes. These child
# processes are seperate from the main interpreter, so their GIL is also seperate. Each child can fully utilize one core. Each
# child has a link to the main process where it receives instructions to do computation and return results.
from time import time

def gcd(pair):
    a, b = pair
    low  = min(a, b)
    for i in range(low, 0, -1):
        if a % i == 0 and b % i == 0:
            return i

# Running this function is serial takes a linearly increasing amount of time because there is no parallelism.
numbers = [(19963309, 2265973), (2030677, 3814172),
           (1551645, 2229620), (2039045, 2020802)]
start   = time()
results = list(map(gcd, numbers))
end     = time()
print(f'Without concurrency it took: {end-start} seconds.')
# Running this code on multiple Python threads will yield no speed improvement because the GIL prevents Python from suing multiple
# CPU cores in paralled, Here I do the same computation as above using concurrent.futures module with its ThreadPoolExecutor class
# and two worker threads (to match the number of CPU cores in my computer)
from concurrent.futures import ThreadPoolExecutor

start   = time()
pool    = ThreadPoolExecutor(max_workers=8)
results = list(pool.map(gcd, numbers))
end     = time()
print(f'With concurrency (ThreadPoolExecutor) it took: {end-start} seconds.')
# When you run it, It's even slower this time because of the overhead of starting and communicating with the pool of threads.

# Now for the surprising part: By changing a single line of code, something magical happens. If I replace the ThreadPoolExecutor with
# the ProcessPoolExecutor from the concurrent.futures module, everything speeds up.
from concurrent.futures import ProcessPoolExecutor

start   = time()
pool    = ProcessPoolExecutor(max_workers=8)
results = list(pool.map(gcd, numbers))
end     = time()
print(f'With concurrency (ProcessPoolExecutor) it took: {end-start} seconds.')

# Running on dual-core machine, It's significintl faster.
# Here's what the ProcessPoolExecutor class actually does (via the low-level constructs provided by the multiprocessing module):
# 1. It takes each item from the numbers input data to map.
# 2. It serializes it into binary data using the pickle module
# 3. It copies the serialized data from the main interpreter process to a child interpreter process over a local soccket.
# 4. Next, It deserializes the data back into Python objects using pickle in the child process.
# 5. It then imports the python module containing the gcd function
# 6. It runs the function on the input data in parallel with other child processes.
# 7. It serializes the result back into bytes.
# 8. It copies those bytes back through the sockets.
# 9. It deserializes the bytes back into Python objects in the parent process.
# 10. Finally, it merges the result form multiple children into a single list to return.

# Although it looks simple to programmers, the multiprocessing module and ProcessPoolExecutor class do a huge amount of work
# to make parallelism  possible. In most other languages, the only touch point you need to coordinate two threads is a single
# lock or atomic operations.


