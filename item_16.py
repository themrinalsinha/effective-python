# Item - 16 : Consider Generator instead of returning lists.

# The simplest choice for functions that produce a sequence of results is to return  a list of items. 
# Eg: you want to find the index of every word in a string. Here, I accumulate result in a list using the append method and return it at the end of the function:

def index_word(text):
    result = []
    if text:
        result.append(0)
    for index, letter in enumerate(text):
        if letter == ' ':
            result.append(index + 1)
    return result

print(index_word('Hello there, how are you ?'))
# there are two problems with the index_words function.
# The first problem is that the code is a bit dense and noisy. Each time a new result is found. I call append method. The method call'es bult (result.append) deemphasizes the value being added to the list (index + 1).

# A better way to write this function is using a generator. Generators are functions that use yield expression. When called, generator funcitons do not actually run but instead immediately return an iterator. With each call to the next built-in function. the iterator will advance the generatorto its next yield expression. Each value passed to yeld by the generator will be rturned by the iterator to the caller.

def index_words_iter(text):
    if text:
        yield 0
        for index, letter in enumerate(text):
            if letter == ' ':
                yield index + 1
print(list(index_words_iter('Hello there, how are you ?')))

# Note:
# -> Using generator can be clearer than the alternative of returning lists of accumulated results.
# -> The iterator returned by a genertor produces the set of values passed to yeld expressions within the generator function's body.
# -> Generator can produce sequence of outupts for aribirarily large inputs because their working memory doesn't include all inputs and outputs. 