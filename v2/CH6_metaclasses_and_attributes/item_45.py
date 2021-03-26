"""
Item 45: Consider @property Instead of refactoring attributes

The built-in @property decorator makes it easy for simple access of an instance's
attributes to smarter.

One advanced but common use of @property is transitioning what was once a simple
numerical attribute into an on-the-fly calculation. This is extremely helpful
because it lets you migrate all existing usage of a class to have new behaviors
without requiring any of the call sites to be rewritten
"""

# I want to implement a leaky bucket quota using plain python objects. Here, the
# Bucket class represents how much quota remains and the duration for which the
# quota will be available:

from datetime import datetime, timedelta

class Bucket:
    def __init__(self, period) -> None:
        self.period_delta = timedelta(seconds=period)
        self.reset_time   = datetime.now()
        self.quota        = 0

    def __repr__(self) -> str:
        return f'Bucket(quota={self.quota})'

# The leaky bucket algorithm works by ensuring that, whenever the bucket is filled,
# the amount of quota does not carry over from one period to the next

def fill(bucket, amount):
    now = datetime.now()
    if (now - bucket.reset_time) > bucket.period_delta:
        bucket.quota = 0
        bucket.reset_time = now
    bucket.quota += amount

# Each time a quota consumer wants to do something, it must first ensure that it can
# deduct the amount of quota it needs to use

def deduct(bucket, amount):
    now = datetime.now()
    if (now - bucket.reset_time) > bucket.period_delta:
        return False # Bucket hasn't been filled this period
    if bucket.quota - amount < 0:
        return False # Bucket was filled, but not enough

    bucket.quota -= amount
    return True # Bucket had enough, quota consumed


bucket = Bucket(60)
fill(bucket, 100)
print(bucket)

if deduct(bucket, 99):
    print('Had 99 quota')
else:
    print('Not enough for 99 quota')
print(bucket)

if deduct(bucket, 3):
    print('Had 3 quota')
else:
    print('Not enough for 3 quota')
print(bucket)
# ===============================================================

"""
The problem with this implementation is that I never know what quota level the bucket
started with. The quota is deducted over the course of the period until it reaches zero.
At that point, deduct will always return False until the bucket is refilled.

When that happens, it would be useful to know whether callers to deduct are being blocked
because the Bucket ran out of quota or because the Bucket never had quota during this period
in that first place.

To fix this, I can change the class to keep track of the max_quota issued in the period
and the quota_consumed in the period:
"""
class NewBucket:
    def __init__(self, period) -> None:
        self.period_delta   = timedelta(seconds=period)
        self.reset_time     = datetime.now()
        self.max_quota      = 0
        self.quota_consumed = 0

    def __repr__(self) -> str:
        return (f'NewBucket(max_quota={self.max_quota},quota_consumed={self.quota_consumed}')

    # To match the previous interface of the original Bucket class, I use a @property method
    # to compute the current level of quota on-the-fly using these new attributes
    @property
    def quota(self):
        return self.max_quota - self.quota_consumed

    # when the quota attribute is assigned, it take special action to be compatible with
    # the current usage of the class by the fill and deduct functions:
    @quota.setter
    def quota(self, amount):
        delta = self.max_quota - amount
        if amount == 0:
            # quota being reset for a new period
            self.quota_consumed = 0
            self.max_quota      = 0

        elif delta < 0:
            # quota being filled for the new period
            assert self.quota_consumed == 0
            self.max_quota = amount

        else:
            # quota being consumed during the period
            assert self.max_quota >= self.quota_consumed
            self.quota_consumed += delta

# re-running the demo code from above produces the same results:
bucket = NewBucket(60)
print('Initial: ', bucket)

fill(bucket, 100)
print('Filled: ', bucket)

if deduct(bucket, 99):
    print('Had 99 quota')
else:
    print('Not enough for 99 quota')

print('Now', bucket)
if deduct(bucket, 3):
    print("Had 3 quota")
else:
    print("Not enough for 3 quota")
print('Still: ', bucket)

"""
Things to Remember
✦ Use @property to give existing instance attributes new functionality.
✦ Make incremental progress toward better data models by using @property.
✦ Consider refactoring a class and all call sites when you find yourself using @property too heavily.
"""
