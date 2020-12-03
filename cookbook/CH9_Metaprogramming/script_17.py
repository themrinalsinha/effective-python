"""
9.23. Executing code with local side effects

Problem: You are using exec() to execute a fragment of code in the scope of the caller,
         but after execution, none of its results seem to be visible.

Solution: To better understand the problem, try a little experiment. First, execute a fragment
          of code in the globe namespace.
"""

a = 13
exec("b = a + 1")
print(a, exec("b = a + 1"))

def test():
    a = 13
    exec('b = a + 1')
    print(b)

test()
# ---------------------------

def test():
    a = 13
    loc = locals()
    exec("b = a + 1")
    b = loc["b"]
    print(b)

test()
# ---------------------------

def test2():
    x = 0
    loc = locals()
    print(f"Before: {loc}")
    exec("x += 1")
    print(f"After: {loc}")
    print(f"x = {x}")

test2()
# ---------------------------

def test3():
    x = 0
    loc = locals()
    print(loc)
    exec('x += 1')
    print(loc)
    locals()
    print(loc)

test3()
# ---------------------------
print('-' * 50)
# ==================================================================================

"""
9.24. Parsing and Analyzing Python Source

Problem: You want to write programs that parse and analyze python source code.

Solution: Most programmers know that python can evaluate or execute source code provided
          in the form of a string.
"""
x = 42
eval('2+3*4+x')
exec('for i in range(10): print(i)')

"""
IMPORTANT: However, the ast module can be used to compile python source code into an
           abstract syntax tree (AST) that can be analyzed.
"""
import ast
ex = ast.parse('2+3*4+x', mode="eval")
print(ex)
print(ast.dump(ex))

# Analyzing the source tree requires a bit of study on your part, but it consists of a col‐
# lection of AST nodes. The easiest way to work with these nodes is to define a visitor
# class that implements various visit_NodeName() methods where NodeName() matches
# the node of interest. Here is an example of such a class that records information about
# which names are loaded, stored, and deleted.

class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self) -> None:
        self.loaded = set()
        self.stored = set()
        self.deleted = set()

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            self.loaded.add(node.id)
        elif isinstance(node.ctx, ast.Store):
            self.stored.add(node.id)
        elif isinstance(node.ctx, ast.Del):
            self.deleted.add(node.id)

# sample usage
if __name__ == "__main__":
    code = """
for i in range(10):
    print(i)
del i
    """

    # parse into an AST
    top = ast.parse(code, mode="exec")

    # feed the AST to analyze name usage
    c = CodeAnalyzer()
    c.visit(top)
    print("Loaded: ", c.loaded)
    print("Stored: ", c.stored)
    print("Deleted: ", c.deleted)

# finally, ASTs can be compiled and executed using the compile() function.
exec(compile(top, '<stdin>', 'exec'))
