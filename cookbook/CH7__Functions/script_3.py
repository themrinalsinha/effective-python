"""
7.9. Replacing single method classes with functions

Problem: You have a class that only defines a single method besides __init__() . However, to
simplify your code, you would much rather just have a simple function.
"""

from urllib.request import urlopen

class UrlTemplate:
    def __init__(self, template) -> None:
        self.template = template

    def open(self, **kwargs):
        return urlopen(self.template.format_map(kwargs))

yahoo = UrlTemplate('http://finance.yahoo.com/d/quotes.csv?s={names}&f={fields}')
for line in yahoo.open(names='IBM,AAPL,FB', fields='sl1c1v'):
    print(line.decode('utf-8'))

# The class could be replaced with a much simpler function:
def urltemplate(template):
    def opener(**kwargs):
        return urlopen(template.format_map(kwargs))
    return opener

yahoo = urltemplate('http://finance.yahoo.com/d/quotes.csv?s={names}&f={fields}')
for line in yahoo(names='IBM,AAPL,FB', fields='sl1c1v'):
    print(line.decode('utf-8'))
