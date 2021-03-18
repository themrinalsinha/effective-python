"""
6.5. Turning a Dictionary to XML

Problem: You want to take the data in Python dictionary and turn it into XML

Solution: Although xml.etree.ElementTree library is commonly used for parsing, it
          can also be used to create XML documents
"""
from xml.etree.ElementTree import Element, tostring

def dict_to_xml(tag, d):
    """
    turning a simple dict of key/value into XML
    """
    elem = Element(tag)
    for key, val in d.items():
        child = Element(key)
        child.text = str(val)

        elem.append(child)
    return elem

s = {'name': 'GOOG', 'shares': 100, 'price': 490.1}
e = dict_to_xml('stock', s)
print(e)
print(tostring(e))
print('- ' * 50)
# ======================================================================================

