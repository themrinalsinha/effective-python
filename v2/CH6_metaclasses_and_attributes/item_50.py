"""
Item 50: Annotate class attributes with __set_name__

one more useful feature enabled by metaclasses is the ability to modify or annotate
properties after a class is defined but before the class is actually used. This approach
is commonly used with descriptors to give them more introspection into how they're being
within their containing class.
"""


# Eg: I want to define a new class that represent a row in a customer database. I'd like
# to have a corresponding property on the class for each column in the database table.
# here, I define a descriptor class to connect attributes to column names:

class Field:
    def __init__(self, name) -> None:
        self.name = name
        self.internal_name = '_' + self.name

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return getattr(instance, self.internal_name, '')

    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)

# Defining the class representing a row requires supplying the database
# table's column name for each class attribute:
class Customer:
    first_name = Field('first_name')
    last_name = Field('last_name')
    prefix = Field('prefix')
    suffix = Field('suffix')

cust = Customer()
print(f"Before: {cust.first_name!r} {cust.__dict__}")

cust.first_name = "Euclid"
print(f"After: {cust.first_name!r} {cust.__dict__}")

# But the class definition seems redundant. I already declared the name of the field
# for the class on the left ('field_name='). why do i also have to pass a string containing
# the same information to the Field constructor on the right ? It looks redundant.

# The Problem is that the order of operations in the Customer class definition is the
# opposite of how it reads from left to right. First the field constructor is called Field('first_name')
# Then, the return value of that is assigned to Customer.field_name. There's no way for a Field instance
# to know upfront which class attribute it will be assigned to.

# To eliminate the redundancy. I can use a metaclass. Metaclass let you hook the class
# statement directly and take action as soon as a class body is finished. In this case I
# can use the metaclass to assign Field.name and Field.internal_name on the descriptor
# automatically instead of manually specifying the field name multiple times:

class Meta(type):
    def __new__(meta, name, bases, class_dict):
        for key, value in class_dict.items():
            if isinstance(value, Field):
                value.name = key
                value.internal_name = '_' + key
        cls = type.__new__(meta, name, bases, class_dict)
        return cls

class DatabaseRow(metaclass=Meta):
    pass

# To work with metaclass, the Field descriptor is largely unchanged. The only difference
# is that it no longer requires arguments to be passed to its constructor. Instead, its
# attributes are set by the Meta.__new__ method above.
class Field:
    def __init__(self) -> None:
        self.name = None
        self.internal_name = None

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return getattr(instance, self.internal_name, '')

    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)

class BetterCustomer(DatabaseRow):
    first_name = Field()
    last_name = Field()
    prefix = Field()
    suffix = Field()

cust = BetterCustomer()
cust.first_name = 'Mrinal'

# ----------------------------------------------------------------------------
# Use the __set_name__ special method for descriptors. This method, introduced, is called
# on every descriptor instance when its containing class is defined. It receives as parameters
# the owning class that contains the descriptor instance and the attribute name to which the
# descriptor instance was assigned. here I avoid defining a metaclass entirely and move what
# the Meta.__new__ method from above was doing into __set_name__.

class Field:
    def __init__(self) -> None:
        self.name = None
        self.internal_name = None

    def __set_name__(self, owner, name):
        # called on class creation for each descriptor
        self.name = name
        self.internal_name = '_' + name

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return getattr(instance, self.internal_name, '')

    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)

class FixedCustomer:
    first_name = Field()
    last_name = Field()

cust = FixedCustomer()
print(cust.first_name)

"""
Things to Remember

✦ Metaclasses enable you to modify a class’s attributes before the
  class is fully defined.

✦ Descriptors and metaclasses make a powerful combination for
  declarative behavior and runtime introspection.

✦ Define __set_name__ on your descriptor classes to allow them to
  take into account their surrounding class and its property names.

✦ Avoid memory leaks and the weakref built-in module by having
  descriptors store data they manipulate directly within a class’s
  instance dictionary.
"""
