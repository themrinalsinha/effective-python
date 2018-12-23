# Initialize parent classes with super

# The old way to initialize a parent class from a child class is to directly call the parent class's __init__ method with the child instance.
# eg:
class MyBaseClass(object):
    def __init__(self, value):
        self.value = value

class MyChildClass(MyBaseClass):
    def __init__(self):
        MyBaseClass.__init__(self, 5)

# This approach works fine for simple hierarchies but breaks down in many cases.
# One problem is that the __init__ call order isn't specified across all subclasses.
# Eg: Here i defined two parent classes that operate on the instance's value field:

class TimesTwo(object):
    def __init__(self):
        self.value *= 2

class PlusFive(object):
    def __init__(self):
        self.value += 5

# This class defines its parent classes in one ordering.
class OneWay(MyBaseClass, TimesTwo, PlusFive):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        TimesTwo.__init__(self)
        PlusFive.__init__(self)
# And constructiongg it produces a result that matches the parent class ordering.
foo = OneWay(5)
print('First ordering is (5 * 2) + 5 = ', foo.value)

# Here another class that defines the same parent classes but in a different ordering.
class AnotherWay(MyBaseClass, PlusFive, TimesTwo):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        TimesTwo.__init__(self)
        PlusFive.__init__(self)
# However, I left the calls to the parent class consturctors PlusFive.__init__ and TimesTwo.__init__ in the same order as before, causing this class's behaviour not to match
# the order of the parent class in its definition.
bar = AnotherWay(5)
print('Second Ordering still is ', bar.value)

# Another problem occur whith diamond inheritance. Diamond inheritance happens when a subclass inherits from two seperate classes
# that have the same superclass somewhere in the hierarchy, diamond inheritance cause this common superclass's __init__ method to run
# multiple times, causing unexpected behaviour. Eg; Here i define two child classes that inherit from MyBaseClass.

class TimesFive(MyBaseClass):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        self.value *= 5

class PlusTwo(MyBaseClass):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        self.value += 2
# Then i define a child class that inherits from both of these classes making MyBaseClass the top of the diamond.
class ThisWay(TimesFive, PlusTwo):
    def __init__(self, value):
        TimesFive.__init__(self, value)
        PlusTwo.__init__(self, value)

foo = ThisWay(5)
print('Should be (5 * 5) + 2 = 27 but is ', foo.value)
# The output should be 27 because (5 * 5) + 2 = 27. But the call to the second parent class's construcctor, PlusTwo.__init__, causes self.value to be
# reset back to 5 when MyBaseClass.__init__ get called a second time.

# To solve this problem, python 2.2 added a super built-in function ad defined the method resolution order (MRO). The MRO standardizes which superclasses are initialized before
# others(eg:. depth-first, left-to-right). It also ensures that common superclasses in diamond hierarchy are only run once.
# Here, I create diamond-shaped class hierarchy again, but this time I use super(in python2 style) to initialize the parent class.
# Python 2

class TimesFiveCorrect(MyBaseClass):
    def __init__(self, value):
        super(TimesFiveCorrect, self).__init__(value)
        self.value *= 5

class PlusTwoCorrect(MyBaseClass):
    def __init__(self, value):
        super(PlusTwoCorrect, self).__init__(value)
        self.value += 2

# Now the top part of the diamond, MyBaseClass.__init__, is only run a single time. The other parent classes are run in the order specified in the class statement.
# python2
class GoodWay(TimesFiveCorrect, PlusTwoCorrect):
    def __init__(self, value):
        super(GoodWay, self).__init__(value)

foo = GoodWay(5)
print('Should be 5 * (5 + 2) = 35 and is ', foo.value)
# This order may seem backwards at first. Shouldn't TimesFiveCorrect.__init__ have run first? Shouldn't the result be (5*5)+2=27?
# The answer is no. This ordering matches what the MRO defines for this class. The MRO orderinng is available on a class method called mro.
from pprint import pprint
pprint(GoodWay.mro())
# When i call GoodWay(5), it in turn calls TimesFiveCorrect.__init__ which calls PlusTwoCorrect.__init__, which calls MyBaseClass.__init__.
# Once this reaches the top of the diamond, then all of the initialization methods actually do their work in the opposite order from how their __init__ functions eere called.
#
# MyBaseclass.__init__ assigns the value to 5. PlusTwoCorrect.__init__ adds 2 to make value equal 7. TimesFiveCorrect.__init__ multiplies it by 5 to make value equal 35.

# =======
# Thankfully, Python3 fixes these issues by making calls to .super with no arguments equivalent to calling super with __class__ and self specified. In python3, you
# should always use super because it's clear. concise and always does the right thing.
class Explicit(MyBaseClass):
    def __init__(self, value):
        super(__class__, self).__init__(value * 2)

class Implicit(MyBaseClass):
    def __init__(self, value):
        super().__init__(value * 2)

assert Explicit(10).value == Implicit(10).value
print(Explicit(10).value == Implicit(10).value)
# This works because Python3 lets you reliably reference the current class in method using the __class__ variable. This doesn't work in python2 because __class__ isn't defined.
# you may guess that you could use self.__class__ as an argument to super, but this breaks because of the way super is implemented in pyton2.
#
# Things to remember:
# --> Python's standard method resolutin order (MRO) solves the problems of superclass initialization order and diamond inheritance.
# --> Always use the super built-in function to initialize parent classes.
