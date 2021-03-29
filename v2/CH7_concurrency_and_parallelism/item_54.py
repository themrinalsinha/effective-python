"""
Item 54: Use Lock to prevent data races in threads

after learning about the GIL, many new python programmers assume they can forgo using
mutual exclusion locks (also called mutexes) in their code altogether. If the GIL is
already preventing python threads from running on multiple CPU cores in parallel, it
must also act as a lock for a programs data structure right ? some testing types like
lists and dictionaries may even show that this assumption appears to hold.

But beware, this is not truly the case. The GIL will not protect you. Although only
one Python thread runs at a time, a thread’s operations on data structures can be
interrupted between any two bytecode instructions in the Python interpreter.
This is dangerous if you access the same objects from multiple threads simultaneously.
The invariants of your data structures could be violated at practically any time
because of these interruptions, leaving your program in a corrupted state.
"""

# Eg: say that i want to write a program that counts many things in parallel, like
# sampling light levels from a whole network of sensors. If i want to determine the
# total number of light samples over time, I can aggregate them with a new class:

class Counter:
    def __init__(self) -> None:
        self.count = 0

    def increment(self, offset):
        self.count += offset

# Imagine that each sensor has its own worker thread because reading from the sensor
# requires blocking I/O. After each sensor measurement, the worker thread increments
# the counter up to a maximum number of desired readings:
import time

def worker(sensor_index, how_many, counter):
    for _ in range(how_many):
        # Reading from the sensor
        # time.sleep(2)

        counter.increment(1)

# Here, I run worker thread for each sensor in parallel and wait for them all to finish
# their readings.
from threading import Thread

how_many = 10**5
counter = Counter()

threads = []
for i in range(5):
    thread = Thread(target=worker, args=(i, how_many, counter))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

expected = how_many * 5
found = counter.count
print(f'Counter should be {expected}, got {found}')

# Python threads incrementing the counter can be suspended between any two of these
# operations. This is problematic if the way the operations interleave causes old
# versions of value to be assigned to the counter. Here’s an example of bad
# interaction between two threads, A and B:
# ------------------------------------------------------------------------------------

# To prevent data races like these, and other forms of data structure corruption, python
# includes a robust set of tools in the threading built-in module. The simplest and most
# useful of them is the Lock class, a mutual-exclusion (mutex)

# By using a lock, I can have the Counter class protect its current value against
# simultaneous accesses from multiple threads. Only one thread will be able to acquire
# the lock at a time. Here, I use a with statement to acquire and release the lock;
# this makes it easier to see which code is executing while the lock is held.

from threading import Lock

class LockingCounter:
    def __init__(self) -> None:
        self.lock  = Lock()
        self.count = 0

    def increment(self, offset):
        with self.lock:
            self.count += offset

# Now, I run the worker threads as before but use a LockingCounter instead:
counter = LockingCounter()

for i in range(5):
    thread = Thread(target=worker, args=(i, how_many, counter))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

expected = how_many * 5
found = counter.count
print(f"Counter should be {expected}, got {found}")

"""
Things to Remember
✦ Even though Python has a global interpreter lock, you’re still
  responsible for protecting against data races between the threads in
  your programs.

✦ Your programs will corrupt their data structures if you allow multiple
  threads to modify the same objects without mutual-exclusion locks (mutexes).

✦ Use the Lock class from the threading built-in module to enforce
  your program’s invariants between multiple threads.
"""
