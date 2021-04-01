def download(item):
    # print(f'[download] - {item}')
    pass

def resize(item):
    # print(f'[resize] - {item}')
    pass

def upload(item):
    # print(f'[upload] - {item}')
    pass


# I can put all these behaviors together into a Queue subclass that also tells the
# worker thread when it should stop processing. Here I define a close method that adds
# a special sentinel item to the queue that indicates there will be no more input item
# after it:

from queue import Queue

class ClosableQueue(Queue):
    SENTINEL = object()

    def close(self):
        self.put(self.SENTINEL)

    # Then, I define an iterator for the queue that looks for this special object and stops
    # iteration when it's found. This __iter__ method also call task_done at appropriate times,
    # letting me track the progress of work on the queue.

    def __iter__(self):
        while True:
            item = self.get()
            try:
                if item is self.SENTINEL:
                    return # cause the thread to exit
                yield item
            finally:
                self.task_done()

# Now, I can redefine my worker thread to rely on the behavior of the CloseQueue class.
# The thread will exit when the for loop is exhausted:

from threading import Thread

class StoppableWorker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func      = func
        self.in_queue  = in_queue
        self.out_queue = out_queue

    def run(self):
        for item in self.in_queue:
            result = self.func(item)
            self.out_queue.put(result)

# I re-create the set worker threads using the new worker class:
download_queue = ClosableQueue()
resize_queue   = ClosableQueue()
upload_queue   = ClosableQueue()
done_queue     = ClosableQueue()

threads = [
    StoppableWorker(download, download_queue, resize_queue),
    StoppableWorker(resize, resize_queue, upload_queue),
    StoppableWorker(upload, upload_queue, done_queue),
]

# After running the worker threads as before, I also send the stop signal after all the
# input work has been injected by closing the input queue of the first phase:

for thread in threads:
    thread.start()

for _ in range(1000):
    download_queue.put(object())

download_queue.close()

# Finally, I wait for the work to finish by joining the queues that connect the phases.
# Each time one phase is done, I signal the next phase to stop by closing its input queue.
# At the end, the done_queue contains all of the output objects, as expected:

download_queue.join()
resize_queue.close()
resize_queue.join()
upload_queue.close()
upload_queue.join()
print(done_queue.qsize(), 'item finished')

for thread in threads:
    thread.join()

# This approach can be extended to use multiple worker threads per phase, which can
# increase I/O parallelism and speed up this type of program significantly. To do this,
# first I define some helper functions that start and stop multiple threads. The way
# stop_threads works is by calling close on each input queue once per consuming thread,
# which ensures that all of the workers exit cleanly:

def start_threads(count, *args):
    threads = [StoppableWorker(*args) for _ in range(count)]
    for thread in threads:
        thread.start()
    return threads

def stop_threads(closable_queue, threads):
    for _ in threads:
        closable_queue.close()
    closable_queue.join()

    for thread in threads:
        thread.join()

# Then, I connect the piece together as before, putting objects to process into the
# top of the pipeline, joining queues and threads along the way, and finally consuming
# the results:
download_queue = ClosableQueue()
resize_queue   = ClosableQueue()
upload_queue   = ClosableQueue()
done_queue     = ClosableQueue()

download_threads = start_threads(3, download, download_queue, resize_queue)
resize_threads   = start_threads(4, resize, resize_queue, upload_queue)
upload_threads   = start_threads(5, upload, upload_queue, done_queue)

for _ in range(1000):
    download_queue.put(object())

stop_threads(download_queue, download_threads)
stop_threads(resize_queue, resize_threads)
stop_threads(upload_queue, upload_threads)

print(done_queue.qsize(), 'item finished')

# Although Queue works well in this case of a linear pipeline, there are many other
# situations for which there are better tools that you should consider

"""
Things to Remember

✦ Pipelines are a great way to organize sequences of work—especially
  I/O-bound programs—that run concurrently using multiple Python
  threads.

✦ Be aware of the many problems in building concurrent pipelines:
  busy waiting, how to tell workers to stop, and potential memory
  explosion.

✦ The Queue class has all the facilities you need to build robust
  pipelines: blocking operations, buffer sizes, and joining.
"""
