"""
Item 60: Achieve Highly concurrent I/O with coroutines


The previous items have tried to solve the parallel I/O problem for the Game of life
example varying degrees of success. All of the other approaches fall short in their
ability to handle thousands os simultaneously concurrent functions.

Python addresses the need for highly concurrent I/O with coroutines. Coroutines let
you have very large number of seemingly simultaneous function in your python programs.
They are implemented using the async and await keywords along with the same infrastructure
that powers generators.

The cost of starting a coroutine is a function call. Once a coroutine is active, it uses
less than 1KB of memory until it's exhausted. Like threads, coroutines are independent
functions that can consume inputs from their environment and produce resulting outputs.

The difference is that coroutines pause at each await expression and resume executing an
async function after the pending awaitable is resolved (similar to how yield behaves in generator)

Many separate async functions advanced in lockstep all seem to run simultaneously, mimicking
the concurrent behavior of python startup and context switching costs, or complex locking and
synchronization code that's required for threads.

The magical mechanism powering coroutines is the event loop which can do highly concurrent
I/O efficiently, while rapidly interleving execution between appropriately written function.
"""
