# Introduction
#
# Metaclass vaguely implies a concept above and beyond a class.
# Simply put, metaclasses let you intercept Python's class statement and provide
# special behaviore each time a class is defined.
#
# Similarly mysterious and powerful are Python's built-in features for dynamically costumizing
# attribute accesses. Along with python's object-oriented constructs, these facilities provide
# wonderful tools to ease the transition from  simple classes to complex ones.
#
# Metaclasses can create extremely bizarre behaviour that are unapproachables to new comers.
# It's import that you follow the rule of least surprise and only use these mechanism to implement
# well understood idioms.

# ITEM 29: Use Plain Attributes Instead of Get and Set Methods.
# ------------------------------------------------------------
# Programmers comming to Python from other languages may naturally try to implement
# explicit getter and setter methods in their classes.

class OldResistor(object):
    def __init__(self, ohms):
        self._ohms = ohms

    def get_ohms(self):
        return self._ohms

    def set_ohms(self, ohms):
        self._ohms = ohms

# Using these setters and getters is simple, but it's not pythonic.
rO = OldResistor(50e3)
print('Before: %5r' % rO.get_ohms())
rO.set_ohms(10e3)
print('After: %5r' % rO.get_ohms())
# Such methods are especially clumsy for operations like incrementing in place.
rO.set_ohms(rO.get_ohms() + 5e3)
print(rO.get_ohms())

# In python, however, you almost never need to implement explicit setter and getter method.
# Instead you should always start your implementation with simple public atributes

print('--------------------------')
class Resistor(object):
    def __init__(self, ohms):
        self.ohms    = ohms
        self.voltage = 0
        self.current = 0

r1 = Resistor(50e3)
print(r1.ohms)
r1.ohms += 5e4
print(r1.ohms)
# This makes operations like incrementing in place natural and clear.

# Later, if you decide you need special behavior when an attribute is set, you can migrate to the @property decorator
# and its corresponding setter attribute. Here I define a new subclass of Resistor what lets me vary the current by
# assigning the voltage property. Note that in order to work properly the name of both the setter and getter methods
# must match the intended property name.

class VoltageResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)
        self._voltage = 0

    @property
    def voltage(self):
        return self._voltage

    @voltage.setter
    def voltage(self, voltage):
        self._voltage = voltage
        self.current = self.voltage / self.ohms

# Now, assigning the voltage property will run the voltage setter method, updting the current property of the object to match.
r2 = VoltageResistance(1e3)
print('Before: %5r amps' % r2.current)
r2.voltage = 10
print('Ater voltage change (current): %5r amps' % r2.current)

# Specifying a setter on a property also lets you perform type checking and validation on values passes to your class. Here
# I define a class that ensure all resistance values are above zero ohms.

class BoundedResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)

    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if ohms <= 0:
            raise ValueError('%f ohms must be > 0' % ohms)
        self._ohms = ohms

    # Assigning an invalid resistance to the attribute raises an exception.

r3 = BoundedResistance(1e3)
# r3.ohms = 0
# an exception will also be raised if you pass an invalid value to the constructor.

# This happens because BoundedResistance.__init__ calls Resistor.__init__, which assigns self.ohms = 0. That assignment causes the
# @ohms.setter method from BoundedResistance to be called, immediately running the validation code before object construction has completed.

# =================================

# You can even use @property to make attributes from parent classes immutable.
class FixedResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)

    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if hasattr(self, '_ohms'):
            raise AttributeError("Can't set attribute")
        self._ohms = ohms
    # Trying to assign to the property after construction raises an exception.
r4 = FixedResistance(1e3)
# r4.ohms = 23 # This will raise Attributte error.
