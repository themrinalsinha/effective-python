"""
2.12. Sanitizing and Clean Up Text

Problem: Some bored script kiddie has enterned the “pýtĥöñ” into a form on your web
         page and you'd like to clean it up somehow.

Solution: The problem of sanitizing and cleaning up text applies to wide variety of
          problems involving text parsing and data handling. At a very simple level,
          you might use basic string functions (eg: str.upper() & str.lower()) to
          convert text to a standard case.
"""
s = 'pýtĥöñ\fis\tawesome\r\n'
print(s)

# The first step is to clean up the whitespace. To do this, make a small translation
# table and use translate()
remap = {
    ord("\t"): ' ',
    ord("\f"): ' ',
    ord("\r"): None # Delete
}

a = s.translate(remap)
print(a)

"""
As you can see here, whitespace character such as \t and \f have been remapped to a
single space. The carriage return \r has been deleted entirely.

You can take this remapping idea a step further and build much bigger tables.
"""
import sys
from sys import maxunicode
import unicodedata
from unicodedata import combining

cmb_chrs = dict.fromkeys(c for c in range(sys.maxunicode) if unicodedata.combining(chr(c)))
b = unicodedata.normalize('NFD', a)
print(b.translate(cmb_chrs))
# OUTPUT: python is awesome

"""
As another example, here is a translaition table that maps all Unicode decimal digit
characters to their equivalent in ASCII
"""
digitmap = { c: ord('0') + unicodedata.digit(chr(c)) for c in range(sys.maxunicode) if unicodedata.category(chr(c)) == 'Nd' }
len(digitmap)

# Arabic Digits
x = '\u0661\u0662\u0663'
print(f"Original: {x}\nMapped: {x.translate(digitmap)}")

"""
Yet another technique for cleaning up text involves I/O decoding and encoding functions.
The idea here is to first do some preliminary cleanup of the text, and then run it through
a combination of encode() or decode() operations to strip or alter it.
"""
a = 'pýtĥöñ is awesome\n'
b = unicodedata.normalize("NFD", a)
print(b.encode("ascii", "ignore").decode("ascii"))
print("- " * 50)
# ===================================================================================

"""
2.13. Aligning Text Strings

Problem: You need to format text with some sort of alignment applied.

Solution: For basic alignment of strings, the ljust(), rjust(), center() methods
          of strings can be used.
"""
# simple justification
text = "hello world"
print("LJUST  : ", text.ljust(20))
print("RJUST  : ", text.rjust(20))
print("CENTER : ", text.center(20))

# justification with padding
text = "hello world"
print("LJUST  : ", text.ljust(20, '-'))
print("RJUST  : ", text.rjust(20, '-'))
print("CENTER : ", text.center(20, '-'))

# The format() function can also be used to easily align things. All you need to do is
# use the <, > or ^ characters along with a desired width. For example:
text = " Mrinal "
print(f"RJUST(>20)  : {text:>20}")
print(f"LJUST(<20)  : {text:<20}")
print(f"CENTER(^20) : {text:^20}")

# print with padding of "="
print(f"RJUST(=>20)  : {text:=>20}")
print(f"LJUST(=<20)  : {text:=<20}")
print(f"CENTER(=^20) : {text:=^20}")

x = 1.2345
print(f"DECIMAL: {x:->10}")
print(f"DECIMAL: {x:-^10.2f}")
print('- ' * 50)
# ==================================================================================
"""
2.15. Interpolating variables in Strings

Problem: You want to create a string in which embedded variable names are substituted with
         a string represention of a variable's value.

Solution: Python has no direct support for simply substituting variable values in strings.
          However, this feature can be approximated using the format() method of strings.
"""
s = '{name} has {n} messages'
print(s.format(name="Mrinal", n=40))

# alternatively, if the values to be substituted are truly found in variables, you can
# use the combination of format_map() and vars(), as in the following
name = "Sinha"
n = 28
print(s.format_map(vars()))

# One subtle feature of vars() is that it also works with instances, Eg:
class Info:
    def __init__(self, name, n) -> None:
        self.name = name
        self.n = n

a = Info("Mrinal", 40)
print(s.format_map(vars(a)))

# One downside of format() and format_map() is that they do not deal gracefully with
# missing values. eg:

# One way to avoid this is to define an alternative dictionary class with a __missing__()
# method, as in the following:
class safesub(dict):
    def __missing__(self, key):
        return '{' + key + '}'

del n # make sure n is undefined
print(s.format_map(safesub(vars())))
