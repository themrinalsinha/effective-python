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
