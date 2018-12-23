# Use Multiple Inheritance only for Mix-in Utility classes.

# Python is an OOP language with built-in facilities for making multiple inheritance tracctable. However it's better to avoid multiple inheritance altogetther.
#
# If you find yourlself desiring the convenience and encapsulation that comes with multiple inheritance, consider writing a mix-instead. A Mix-in
# is a small class that only defines a set of additional methods that a class should provide.
# Mix-in classses don't define their own instance attributes not require their __init__ constructor to be called.
#
# Writing Mix-ins is easy beecause Python makes trivial to inspect the current state of any object regardless of its tupe.
# Dynamic inspection lets you write generic functionality a single time, in a mix-in, that can be applied to many other classes.
# Mix-ins can be composed and layered to minimize repetitive code and maximize reuse
#
# Eg: say you want the ability to convert a python object from its in-memory representation to a dictionary that's ready for serialization.
# Why not write this functioality generically so you can use it with all your classes?
#
# Here I define an example mix-in that accomplishes this with a new public method that's added to any classs that inherits from it.

class ToDictMixin(object):
    def to_dict(self):
        return self._traverse_dict(self.__dict__)

    # The implementation details are straightforward and rely on dynamic attribute access using hasattr, dynamic type inspection with
    # isinstance, and assessing the instance dictonary __dict__.

    def _traverse_dict(self, instance_dict):
        output = {}
        for key, value in instance_dict.items():
            output[key] = self._traverse(key, value)
        return output

    def _traverse(self, key, value):
        if isinstance(value, ToDictMixin):
            return value.to_dict()
        elif isinstance(value, dict):
            return self._traverse_dict(value)
        elif isinstance(value, list):
            return [self._traverse(key, i) for i in value]
        else:
            return value

# Here, I defined an example class that uses the mix-in to make a dictionary representation of a binary tree:
class BinaryTree(ToDictMixin):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left  = left
        self.right = right

# Translating a large number of related Python object into a dictonary becomes easy.
tree = BinaryTree(10,
                  left=BinaryTree(7, right=BinaryTree(9)),
                  right=BinaryTree(13, left=BinaryTree(11)))
print(tree.to_dict())

# The best part about mix-ins is that you can make their generic functionality pluggable so behaviors can be overridden when required.
# For example, here I define a subclass of binaryTree that holds a reference to its parent. this circular refence would cause the default
# implementation to ToDictMixin.to_dict to loop forever.

class BinaryTreeWithParent(BinaryTree):
    def __init__(self, value, left=None, right=None, parent=None):
        super().__init__(value, left=left, right=right)
        self.parent = parent

    # The solution is to override the ToDictMixin._traverse method in the BinaryTreeWithParent class to only process values that matter, preventing
    # cycles to encountered by the mix-in. Here I override the _traverse mehtod to not traverse the parent and just insert its numerical value.

    def _traverse(self, key, value):
        if (isinstance(value, BinaryTreeWithParent) and key == 'parent'):
            return value.value # prevent cycles
        else:
            return super()._traverse(key, value)

    # Calling BinaryTreeWithParent.to_dict will work without issue because the curcular referencing properties aren't followed.
root = BinaryTreeWithParent(10)
root.left = BinaryTreeWithParent(7, parent=root)
root.left.right = BinaryTreeWithParent(9, parent=root.left)
print(root.to_dict())

# By defining BinaryTreeWithParent._traverse, We have also enabled any class that has an attribute of type BinaryTreeWithParent to automatically
# work with ToDictMixin.

class NamedSubTree(ToDictMixin):
    def __init__(self, name, tree_with_parent):
        self.name = name
        self.tree_with_parent = tree_with_parent

my_tree = NamedSubTree('foobar', root.left.right)
print(my_tree.to_dict())

# Mix-ins can also be composed together. For example, say you want a mix-in that provides generic JSON Serialization for any class.
# You can do this by assuming that a class provides a to_dict method (which ay or may not be provided by the ToDictMixin class).

import json
class JsonMixin(object):
    @classmethod
    def from_json(cls, data):
        kwargs = json.loads(data)
        return cls(**kwargs)

    def to_json(self):
        return json.dumps(self.to_dict())

    # Note how the JsonMixin class defines both instance methods and class methods. Mix-ins let you add either kind of behavior. In this example, the
    # only requirements of the JsonMixin are that the class has a to_dict method and its __init__ mehtod takes keyword arguments.

    # This mix-in makes it simple to create hierarchies of utility classes that can be serialized to and from JSON with little boilerplate.
    # For example, here we have a hierarchy of data classes representing parts of a datacenter topology.


class DatacenterRack(ToDictMixin, JsonMixin):
    def __init__(self, switch=None, machines=None):
        self.switch = Switch(**switch)
        self.machines = [Machine(**kwargs) for kwargs in machines]
class Switch(ToDictMixin, JsonMixin):
    # ......
    # ......
    pass
class Machine(ToDictMixin, JsonMixin):
    # ......
    # ......
    pass

# Serializing these classes to and from JSON is simple. Here I verify that the data is able to be sent round-trip through serializing and deserializing.

serialized = """
{"switch": {"ports": 5, "speed": 1e9},
"machines": [
    {"cores": 8, "ram": 32e9, "disk": 5e12},
    {"cores": 4, "ram": 16e9, "disk": 1e12},
    {"cores": 2, "ram": 4e9, "disk": 500e9}
]}"""

# desearilize = DatacenterRack.from_json(serialized)
# roundtrip = desearilize.to_json()
# print(roundtrip)


# When you use mix-ins like this it's also fine if the class already inherits from JsonMixin higher up in the ojbect hierarchy. The resulting class will behave the same way.
# Things to remembeer:
# --> Avoid uisng multiple inheritance if mix-in classes can achieve the same outcome.
# --> Use pluggable behaviours at the instance level to provice pre-class customization when mix-in classes may require it.
# --> compose mix-ins to create complex functionality from simple behaviours.
