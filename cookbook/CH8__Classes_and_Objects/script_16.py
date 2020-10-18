"""
8.21. Implementing the visitor pattern

Problem: You need to write code that processes or navigates through a complicated data structure
consisting of many different kinds of objects, each of which needs to be handled in a
different way. For example, walking through a tree structure and performing different
actions depending on what kind of tree nodes are encountered.

Solution: The problem addressed by this recipe is one that often arises in programs that build
data structures consisting of a large number of different kinds of objects. To illustrate,
suppose you are trying to write a program that represents mathematical expressions.
To do that, the program might employ a number of classes
"""

class Node:
    pass

class UnaryOperator(Node):
    def __init__(self, operand) -> None:
        self.operand = operand

class BinaryOperator(Node):
    def __init__(self, left, right) -> None:
        self.left  = left
        self.right = right

class Add(BinaryOperator):
    pass

class Sub(BinaryOperator):
    pass

class Mul(BinaryOperator):
    pass

class Div(BinaryOperator):
    pass

class Negate(UnaryOperator):
    pass

class Number(Node):
    def __init__(self, value) -> None:
        self.value = value

# Representation of 1 + 2 * (3 - 4) / 5
t1 = Sub(Number(3), Number(4))
t2 = Mul(Number(2), t1)
t3 = Div(t2, Number(5))
t4 = Add(Number(1), t3)

"""
The problem is not the creation of such structures, but in writing code that processes
them later. For example, given such an expression, a program might want to do any
number of things

To enable general-purpose processing, a common solution is to implement the so-called
“visitor pattern”
"""
class NodeVisitor:
    def visit(self, node):
        methname = 'visit_' + type(node).__name__
        meth = getattr(self, methname, None)
        if not meth:
            meth = self.generic_visit
        return meth(node)

    def generic_visit(self, node):
        raise RuntimeError(f"No visit_{type(node).__name__} method")

# To use this class, a programmer inherits from it and implements various methods of the
# form visit_Name() , where Name is substituted with the node type. For example, if you
# want to evaluate the expression, you could write this:

class Evaluator(NodeVisitor):
    def visit_Number(self, node):
        return node.value

    def visit_Add(self, node):
        return self.visit(node.left) + self.visit(node.right)

    def visit_Sub(self, node):
        return self.visit(node.left) - self.visit(node.right)

    def visit_Mul(self, node):
        return self.visit(node.left) * self.visit(node.right)

    def visit_Div(self, node):
        return self.visit(node.left) / self.visit(node.right)

    def visit_Negate(self, node):
        return -node.operand

# Here is an example of how you would use this class using the previously generated
# expression:
e = Evaluator()
print(f"T4 => {e.visit(t4)}")

# As a completely different example, here is a class that translate an expression
# into operations on a simple stack machine
class StackCode(NodeVisitor):
    def generate_code(self, node):
        self.instructions = []
        self.visit(node)
        return self.instructions

    def visit_Number(self, node):
        self.instructions.append(('PUSH', node.value))

    def binop(self, node, instruction):
        self.visit(node.left)
        self.visit(node.right)
        self.instructions.append((instruction,))

    def visit_Add(self, node):
        self.binop(node, 'ADD')

    def visit_Sub(self, node):
        self.binop(node, 'SUB')

    def visit_Mul(self, node):
        self.binop(node, 'MUL')

    def visit_Div(self, node):
        self.binop(node, 'DIV')

    def unaryop(self, node, instruction):
        self.visit(node.operand)
        self.instructions.append((instruction,))

    def visit_Negate(self, node):
        self.unaryop(node, 'NEG')

s = StackCode()
print(s.generate_code(t4))

# There are really two key ideas in this recipe. The first is a design strategy where code
# that manipulates a complicated data structure is decoupled from the data structure itself.
# That is, in this recipe, none of the various Node classes provide any implementation that
# does anything with the data. Instead, all of the data manipulation is carried out by
# specific implementations of the separate NodeVisitor class. This separation makes the
# code extremely general purpose.

