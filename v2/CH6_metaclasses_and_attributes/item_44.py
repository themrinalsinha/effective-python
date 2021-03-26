# ====================================================================================
"""
Metaclasses are often mentioned in lists of python's features, but few understand
what they accomplish in practice. The name metaclass vaguely implies a concept above
and beyond a class. Simply put, metaclasses let you intercept python's class statement
and provide special behavior each time a class is defined.

Similarly mysterious and powerful are python's built-in features  for dynamically
customizing attribute access. Along with python's object-oriented constructs, these
facilities provide wonderful tools to ease the transaction from simple classes to
complex ones.
"""
# ====================================================================================

"""
Item 44: Use plain attributes instead of setter and getter methods
"""
# programmers coming to python from other languages may naturally try to implement
# explicit getter and setter methods in their classes

class OldResistor:
    def __init__(self, ohms) -> None:
        self._ohms = ohms

    def get_ohms(self):
        return self._ohms

    def set_ohms(self, ohms):
        self._ohms = ohms

# Using these setters and getters is simple, but it's not pythonic:
r0 = OldResistor(50e3)
print('Before: ', r0.get_ohms())
r0.set_ohms(10e3)
print('After: ', r0.get_ohms())
# such methods are especially clumsy for operations like incremeting in place:
r0.set_ohms(r0.get_ohms() - 4e3)
assert r0.get_ohms() == 6e3


# These utility methods do, however, help define the interface for
# a class, making it easier to encapsulate functionality, validate usage,
# and define boundaries. Those are important goals when designing a
# class to ensure that you don’t break callers as the class evolves over
# time.

class Resistor:
    def __init__(self, ohms) -> None:
        self.ohms = ohms
        self.voltage = 0
        self.current = 0

r1 = Resistor(50e3)
r1.ohms = 10e3

# These attributes make operations like incrementing in place natural and clear
r1.ohms += 5e3

# Later, If i decide I need special behavior when an attribute is set, I can
# migrate to the @property decorator. Define function decorators with functools.wraps
# for behavior and its corresponding setter attribute

class VoltageResistance(Resistor):
    def __init__(self, ohms) -> None:
        super().__init__(ohms)
        self._voltage = 0

    @property
    def voltage(self):
        return self._voltage

    @voltage.setter
    def voltage(self, voltage):
        self._voltage = voltage
        self.current = self._voltage / self.ohms

# Now, assigning the voltage property will run the voltage setter method,
# which in turn will update the current attribute of the object to match:

r2 = VoltageResistance(1e3)
print(f"Before: {r2.current:.2f} amps")

r2.voltage = 10
print(f"After: {r2.current:.2f} amps")

# specifying a setter on a property also enables me to perform type checking
# and validation on values passed to the class. Here I define a class that
# ensures all resistance values are above zero ohms

class BoundedResistance(Resistor):
    def __init__(self, ohms) -> None:
        super().__init__(ohms)

    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if ohms <= 0:
            raise ValueError(f"Ohms must be > 0; got {ohms}")
        self._ohms = ohms

# I can even use @property to make attribute from parent classes immutable
class FixedResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)

    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if hasattr(self, '_ohms'):
            raise AttributeError("Ohms is immutable")
        self._ohms = ohms

r4 = FixedResistance(1e3)
# r4.ohms = 2e3 # it will throw error...

"""
Things to Remember
✦ Define new class interfaces using simple public attributes and avoid
  defining setter and getter methods.
✦ Use @property to define special behavior when attributes are
  accessed on your objects, if necessary.
✦ Follow the rule of least surprise and avoid odd side effects in your
  @property methods.
✦ Ensure that @property methods are fast; for slow or complex work—
  especially involving I/O or causing side effects—use normal meth-
  ods instead.
"""
