"""
Item 6: Prefer multiple assignment unpacking over indexing
"""
# Python has built-in tuple type that can be used to create immutable, ordered
# sequences of values. In the simplest case, a tuple is a pair of two values,
# such as keys and values from a dictionary

snack_calories = {
    'chips': 140,
    'popcorn': 80,
    'nuts': 190,
}

items = tuple(snack_calories.items())
print(items)

fav_snacks = {
    'salty': ('pretzels', 100),
    'sweet': ('cookies', 180),
    'veggie': ('carrors', 20),
}

(
    (type_1, (name_1, cals_1)),
    (type_2, (name_2, cals_2)),
    (type_3, (name_3, cals_3)),
) = fav_snacks.items()

print(type_1, name_1, cals_1)
print(type_2, name_2, cals_2)
print(type_3, name_3, cals_3)
