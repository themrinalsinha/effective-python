"""
Item 53: Use Threads for Blocking I/O, Avoid for parallelism


The standard implementation of python is called CPython. CPython runs a python program
in two steps. First it parses and compiles the source text into bytecode, which is a
low-level representaton of the program as 8-bit instructions. Then CPython runs the
bytecode using a stack-based interpreter. The bytecode interpreter has state that must
be maintained and coherent while the Python program executes. CPython enforces coherence
with a mechanism called the global interpreter lock (GIL).

Essentially, the GIL is a mutual-exclusion lock (mutex) that prevents CPython from being
affected by preemptive multithreading, where one thread takes control of a program by
interrupting another thread. Such as interruption could corrupt the interpreter state
if it comes at an unexpected time. The GIL prevents these interruptions and ensures that
every bytecode instruction works correctly with the CPython implementation and its
C-extension modules.

The GIL has an important negative side effect. With programs written in languages like C++
or JAVA, having multiple threads of execution means that a program could utilize multiple
CPU cores at the same time. Although Python supports multiple threads of execution, the GIL
causes only one of the them to ever make forward progress at a time. This means that when
you reach for thread to do parallel computation and speed up your programs, you will be
sorely disappointed.
"""

# Eg: say that i want to do something computationally intensive with python. Here i use
#     a native number factorization algorithm as a proxy

def factorize(number):
    for i in range(1, number + 1):
        if number % i == 0:
            yield i

# Factorizing a set of numbers in serial takes quite a long time

import time

numbers = [2139079, 1214759, 1516637, 1852285]

start = time.time()
for number in numbers:
    list(factorize(number))
end = time.time()
delta = end-start
print(f"[serial execution] Took {delta:.3f} seconds")


# Using multiple threads to do this computation would make sense in other languages
# because i could take advantage of all the CPU cores of my computer. Let my try that
# in python. Here i define a python thread for doing the same computation as before:
from threading import Thread

class FactorizeThread(Thread):
    def __init__(self, number):
        super().__init__()
        self.number = number

    def run(self):
        self.factors = list(factorize(self.number))

# Then, I start a thread for each number to factorize in parallel.
start = time.time()

threads = []

for number in numbers:
    thread = FactorizeThread(number)
    thread.start()
    threads.append(thread)

# finally, I wait for all of the threads to finish:
for thread in threads:
    thread.join()

end = time.time()
delta = end - start
print(f"[thread execution] Took {delta:.3f} seconds")

"""
Surprisingly, this takes even longer than running factorize in serial with one thread
per number, you might expect less than 4x speeup in other languages due to the overhead
of creating threads and coordinating with them. You might expect only a 2x speedup on
the dual core machine I used to run this code. But you wouldn't expect the performace
of these threads to be worse when there are multiple CPUs to utilize. This demonstrate
the effect of the GIL (eg: lock content and schedule overhead) on programs running in
the standard CPython interpreter.

There are ways to get CPython to utilize multiple cores, but they don't work with the
standard Thread class and they can require substantial effort. Given these limitations,
why does python support threads at all ? There are two good reasons

First, multiple threads make it easy for a program to seem like it’s doing multiple
things at the same time. Managing the juggling act of simultaneous tasks is difficult
to implement yourself. With threads, you can leave it to Python to run your functions
concurrently. This works because CPython ensures a level of fairness between Python
threads of execution, even though only one of them makes forward progress at a time
due to the GIL.

Second, Python supports threads is to deal with blocking I/O, which happens when
Python does certain types of system calls. A Python program uses system calls to
ask the computer’s operating system to interact with the external environment on
its behalf. Blocking I/O includes things like reading and writing files, interacting
with networks, communicating with devices like displays, and so on. Threads help
handle blocking I/O by insulating a program from the time it takes for the operating
system to respond to requests.
"""

# Eg, say that i want to send a signal to a remote-controlled helicopter through a
#     serial port. I'll use a slow system call (select) as a proxy for this activity.
#     The function asks the operating system to block for 0.1 seconds and then return
#     control to my program, which is similar to what would happen when using a
#     synchronous serial port:

import select
import socket

def slow_systemcall():
    select.select([socket.socket()], [], [], 0.5)

# Running this system call in serial requires a linearly increasing amount of time:

start = time.time()
for _ in range(5):
    slow_systemcall()
end = time.time()
delta = end - start
print(f'[using select] took {delta:.3f} seconds')

# The problem is that while the slow_systemcall function is running, my
# program can’t make any other progress. My program’s main thread of
# execution is blocked on the select system call. This situation is awful
# in practice. You need to be able to compute your helicopter’s next move
# while you’re sending it a signal; otherwise, it’ll crash. When you find
# yourself needing to do blocking I/O and computation simultaneously,
# it’s time to consider moving your system calls to threads.

# Here, I run multiple invocations of the slow_systemcall function in
# separate threads. This would allow me to communicate with multiple
# serial ports (and helicopters) at the same time while leaving the main
# thread to do whatever computation is required:

start = time.time()
threads = []
for _ in range(5):
    thread = Thread(target=slow_systemcall)
    thread.start()
    threads.append(thread)

# with the threads started, here i do some work to calculate the next helicopter move
# before waiting for the system call threads to finish.
def compute_helicopter_location(index):
    pass

for i in range(5):
    compute_helicopter_location(i)

for thread in threads:
    thread.join()

end = time.time()
delta = end - start
print(f"TOok {delta:.3f} seconds")

"""
The parallel time is ~5x less than the serial time. This shows that
all the system calls will run in parallel from multiple Python threads
even though they’re limited by the GIL. The GIL prevents my Python
code from running in parallel, but it doesn’t have an effect on system
calls. This works because Python threads release the GIL just before
they make system calls, and they reacquire the GIL as soon as the
system calls are done.

There are many other ways to deal with blocking I/O besides using
threads, such as the asyncio built-in module, and these alternatives
have important benefits. But those options might require extra work
in refactoring your code to fit a different model of execution (see Item
60: “Achieve Highly Concurrent I/O with Coroutines” and Item 62:
“Mix Threads and Coroutines to Ease the Transition to asyncio ”).
Using threads is the simplest way to do blocking I/O in parallel with
minimal changes to your program.
"""

"""
Things to Remember
✦ Python threads can’t run in parallel on multiple CPU cores because
  of the global interpreter lock (GIL).

✦ Python threads are still useful despite the GIL because they provide
  an easy way to do multiple things seemingly at the same time.

✦ Use Python threads to make multiple system calls in parallel. This
  allows you to do blocking I/O at the same time as computation.
"""
