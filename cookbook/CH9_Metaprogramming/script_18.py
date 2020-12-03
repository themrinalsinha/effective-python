"""
9.25. Disassembling Python Byte Code

Problem: You want to know in detail what your code is doing under the covers by
         disassembling in into lower-level byte code used by the interpreter.

Solution: The dis module can be used to output a disassembly of any Python function.
"""
import dis
import opcode

def countdown(n):
    while n > 0:
        print('T-minus', n)
        n -= 1
    print("Blastoff!")

dis.dis(countdown)
c = countdown.__code__.co_code

print('- ' * 50)
print(opcode.opname[c[0]])
print(opcode.opname[c[1]])
print(opcode.opname[c[2]])
print('- ' * 50)
# ==================================================================================

import opcode

def generate_opcodes(codebytes):
    extended_arg = 0
    i = 0
    n = len(codebytes)

    while i < n:
        op = codebytes[i]
        i += 1
        if op >= opcode.HAVE_ARGUMENT:
            oparg = codebytes[i] + codebytes[i+1]*256 + extended_arg
            extended_arg = 0
            i += 2

            if op == opcode.EXTENDED_ARG:
                extended_arg = oparg * 65536
                continue
        else:
            oparg = None
        yield (op, oparg)

# To use this function, you would use code like this:
for op, oparg in generate_opcodes(countdown.__code__.co_code):
    print(op, opcode.opname[op], oparg)

print()
def add(x, y):
    return x + y

c = add.__code__
print(c)
