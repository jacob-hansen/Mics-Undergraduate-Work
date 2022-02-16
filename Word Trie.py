# NO ADDITIONAL IMPORTS!
import doctest
from text_tokenize import tokenize_sentences


class Trie:
    def __init__(self, key_type):
        self.children = {}
        self.key_type = key_type
        self.value = None

    def __setitem__(self, key, value):
        """
        Add a key with the given value to the trie, or reassign the associated
        value if it is already present in the trie.  Assume that key is an
        immutable ordered sequence.  Raise a TypeError if the given key is of
        the wrong type.

        >>> myTrie = Trie(str)
        >>> myTrie['hello'] = 'world'
        >>> myTrie = Trie(int)
        >>> myTrie['hello'] = 'world'
        raises TypeError
        """
        if type(key) != self.key_type: # raise TypeError if wrong type key
            raise TypeError

        if len(key) == 0: # base case is where we reach the node where the key points, thus len(key) == 0 => True
            self.value = value
        elif (key[0:1] in self.children): # recursive calls below are used to find the trie who's root is the key's position
            nextKey = self.children[self.key_type(key[0:1])]
            nextKey.__setitem__(self.key_type(), value) if len(key) == 1 else nextKey.__setitem__(key[1:], value)
        else:
            nextKey = Trie(self.key_type)
            nextKey.__setitem__(self.key_type(), value) if len(key) == 1 else nextKey.__setitem__(key[1:], value)

            self.children[key[0:1]] = nextKey
        pass # no need to return anything

    def __getitem__(self, key):
        """
        Return the value for the specified prefix.  If the given key is not in
        the trie, raise a KeyError.  If the given key is of the wrong type,
        raise a TypeError.
        >>> myTrie = Trie(str)
        >>> myTrie['hello'] = 'world'
        >>> print(myTrie['hello'])
        world
        """
        if type(key) != self.key_type: # raise TypeError if wrong type key
            raise TypeError

        if not key:
            if self.value != None: # base case is where we reach the node where the key points, thus not key => True
                return self.value
            else:
                raise KeyError

        if (len(key) != 0 and key[0:1] in self.children): # this recursivly calls __getitem__ to find the key's position
            if len(key) == 1:
                return self.children[key[0:1]][self.key_type()]
            return self.children[key[0:1]][key[1:]]
        raise KeyError # this is because the key was not in self.children, thus it is not in the tree



    def __delitem__(self, key):
        """
        Delete the given key from the trie if it exists. If the given key is not in
        the trie, raise a KeyError.  If the given key is of the wrong type,
        raise a TypeError.
        >>> myTrie = Trie(str)
        >>> myTrie['hello'] = 'world'
        >>> print(myTrie['hello'])
        world
        >>> del(myTrie['hello'])
        raises KeyError
        """
        if type(key) != self.key_type: # raise TypeError if wrong type key
            raise TypeError

        if not key: # base case is where we reach the node where the key points, thus not key => True
            if self.value != None:
                self.value = None
            else:
                raise KeyError
            return

        if (len(key) != 0 and key[0:1] in self.children): # this recursivly calls __delitem__ to find the key's position
            if len(key) == 1:
                self.children[key[0:1]].__delitem__(self.key_type())
                return
            self.children[key[0:1]].__delitem__(self.key_type(key[1:]))
            return
        raise KeyError # this is because the key was not in self.children, thus it is not in the tree

    def __contains__(self, key):
        """
        Is key a key in the trie? return True or False.  If the given key is of
        the wrong type, raise a TypeError.
        >>> myTrie = Trie(str)
        >>> myTrie['hello'] = 'world'
        >>> 'hello' in myTrie
        True
        >>> 'bear' in myTrie
        False
        """
        if type(key) != self.key_type:
            raise TypeError
        try:
            self[key]
        except KeyError: return False
        except TypeError: raise TypeError
        return True

    def __iter__(self, prev_keys = False):
        """
        Generator of (key, value) pairs for all keys/values in this trie and
        its children.  Must be a generator!
        >>> myTrie = Trie(str)
        >>> myTrie['hello'] = 1
        >>> myTrie['h'] = 2
        >>> myTrie['ar'] = 3
        >>> myTrie['world'] = 4
        >>> myTrie['mess'] = 5
        >>> print(next(iter(myTrie)))
        ('h', 2)
        """
        if prev_keys == False:
            prev_keys = self.key_type()

        if self.value != None: # this lines create a generator that returns items one at a time
            yield (prev_keys, self.value)
        for num in self.children:
            for value in self.children[num].__iter__(self.key_type(prev_keys+num)):
                yield value



def make_word_trie(text):
    """
    Given a piece of text as a single string, create a Trie whose keys are the
    words in the text, and whose values are the number of times the associated
    word appears in the text
    >>> theTrie = make_word_trie('this is a long text where we want to create a word tree for all the words in this text. a a a ')
    >>> print(theTrie['a'])
    5
    >>> print(theTrie['text'])
    2
    """
    myTrie = Trie(str)
    sentences = tokenize_sentences(text) # break up text into sentences
    words = []
    for sentence in sentences:
        to_add = sentence.split() # break up sentences into words
        for word in to_add:
            words.append(word)
    for word in words: # add words to trie and return the trie
        if word in myTrie:
            myTrie[word] += 1
        else:
            myTrie[word] = 1
    return myTrie

def make_phrase_trie(text):
    """
    Given a piece of text as a single string, create a Trie whose keys are the
    sentences in the text (as tuples of individual words) and whose values are
    the number of times the associated sentence appears in the text.
    >>> theTrie = make_phrase_trie('Test sentence. Test sentence. What to do. This is a lot of senences. Hello!')
    >>> print(theTrie['test sentence'])
    2
    """
    myTrie = Trie(tuple)
    sentences = tokenize_sentences(text) # split up the text into sentences
    finalList = []
    for sentence in sentences:
        finalList.append(tuple(sentence.split())) # split the sentences by their words
    for word in finalList: # add them to a trie that is returned
        if word in myTrie:
            myTrie[word] += 1
        else:
            myTrie[word] = 1
    return myTrie


def autocomplete(trie, prefix, max_count=None):
    """
    Return the list of the most-frequently occurring elements that start with
    the given prefix.  Include only the top max_count elements if max_count is
    specified, otherwise return all.

    Raise a TypeError if the given prefix is of an inappropriate type for the
    trie.

    >>> theTrie = make_word_trie('this is a long text where we want to create a word tree for all the words in this text I wanted to find wanderer wandering wanderer wanderer wanker wanderingly')
    >>> print(autocomplete(theTrie, 'wan'))
    ['wanderer', 'want', 'wanted', 'wandering', 'wanderingly', 'wanker']
    >>> print(autocomplete(theTrie, 'wan', 2))
    ['wanderer', 'want']
    """
    if type(prefix) != trie.key_type: # raise TypeError if the key is of the wrong type
        raise TypeError

    if len(prefix) == 0: # base case for recursive call. Returns a sorted list of length < max_count
        values = []
        for i in trie:
            values.append(i)
        values.sort(key = lambda x: -x[1])
        returnList = [i[0] for i in values]
        if max_count != None:
            return returnList[0:max_count]
        else:
            return returnList

    elif (prefix[0:1] in trie.children): # call recursivly to find base case
        if len(prefix) == 1:
            answer = autocomplete(trie.children[prefix[0:1]], trie.key_type(), max_count)
        else:
            answer = autocomplete(trie.children[prefix[0:1]], prefix[1:], max_count)
        return [prefix[0:1]+i for i in answer]
    else:
        return []


def autocorrect(trie, prefix, max_count=None):
    """
    Return the list of the most-frequent words that start with prefix or that
    are valid words that differ from prefix by a small edit.  Include up to
    max_count elements from the autocompletion.  If autocompletion produces
    fewer than max_count elements, include the most-frequently-occurring valid
    edits of the given word as well, up to max_count total elements.


    >>> theTrie = make_word_trie('this is a long text where we want to create a word tree for all the words in this text I wanted to find wanderer wandering wanderer wanderer wanker wanderingly')
    >>> print(autocorrect(theTrie, 'wander', 1))
    ['wanderer']
    >>> print(autocorrect(theTrie, 'waneer', 1))
    ['wanker']
    """
    if (max_count == 0):
        return []
    test = autocomplete(trie, prefix, max_count)
    if max_count == None or len(test) > max_count:
        return test

    edits = set()
    letters = list("abcdefghijklmnopqrstuvwxyz")
    key = tuple(i for i in prefix)

    for i in range(len(key)+1): # for adding, removing, swapping, or changing each letter
        if i+1 < len(key):
            edits.add(key[0:i]+key[i+1:]) # for removing a letter
            if i+2 < len(key):
                edits.add(key[0:i]+(key[i+1],)+(key[i],)+key[i+2:]) # for swapping two letters
            else:
                edits.add(key[0:i]+(key[i+1],)+(key[i],)) # for swapping two letters
        elif i == len(key):
            edits.add(key[0:i]) # for removing a letter
        for letter in letters:
            if i+1 < len(key):
                edits.add(key[0:i]+(letter,)+key[i+1:]) # for changing a letter
                edits.add(key[0:i]+(letter,)+key[i:]) # for adding a letter
            elif i+1 == len(key):
                edits.add(key[0:i]+(letter,)) # for changing a letter
                edits.add(key[0:i]+(letter,)+key[i:]) # for adding a letter
            else:
                edits.add(key+(letter,)) # for adding a letter
    additional = set()
    for edit in edits:
        if ''.join(edit) in trie:
            additional.add(''.join(edit))
    additional = list(additional)
    additional.sort(key = lambda x: -trie[x])
    for i in additional: # for every mutation we found and checked that is a proper word, we now add it to the test list
        if i not in test:
            test.append(i)
        if (len(test) == max_count):
            return list(test)
    return list(test)




def word_filter(trie, pattern, word = ''):
    """
    Return list of (word, freq) for all words in trie that match pattern.
    pattern is a string, interpreted as explained below:
         * matches any sequence of zero or more characters,
         ? matches any single character,
         otherwise char in pattern char must equal char in word.
    """
    returnList = []
    for letter in trie.children:
        if match(str(word+letter), pattern, True):
            returnList.append(word_filter(trie.children[letter], pattern, str(word+letter)))
            if str(word+letter) in trie:
                returnList.append(str(word+letter))
    return returnList

def match(word, pattern, cut_short = False):
    """
    this returns whether or not a word matches the pattern.
    If cut_short is set to True, if there is any possible character(s) that could be appended to make match, it returns True
    """
    subword = word[:]
    await_next = False
    for i in pattern:
        if i == '*':
            await_next = True # this is for when we need to skip characters for the '*'
            continue
        if (len(subword) > 0):
            if await_next == True:
                while(True):
                    if subword[0] == i or i == '?': # if it is the correct letter, we can move on
                        if len(subword) == 1:
                            subword = ''
                        else:
                            subword = subword[1:]
                        await_next = False
                        break
                    if len(subword) == 1:
                        subword = ''
                        break
                    else:
                        subword = subword[1:]
                continue
            else: # if await_next is not True, then we can just check if its the right letter
                if subword[0] == i or i == '?':
                    if len(subword) == 1:
                        subword = ''
                    else:
                        subword = subword[1:]
                    continue
                return False
        else:
            if cut_short:
                return True
            elif i != '*':
                return False
            continue
    if len(subword) > 0 and await_next == False:
        return False
    return True

def codeQuestion1():
    """
    prints out answers to the questions in the lab
    """
    with open("alicewonderland.txt", encoding="utf-8") as f:
        text = f.read()
    myTrie = make_phrase_trie(text)
    get_frases = [('hello', 0) for i in range(6)]
    for i in myTrie:
        if i[1] > get_frases[0][1]:
            get_frases[0] = i
            get_frases.sort(key=lambda x: x[1])
    print("Alice in wonderland 6 most common sentences are: ")
    print(tuple([i[0] for i in get_frases]))  # => evaluates to ('beauootiful soooop', 'said the march hare', 'said the caterpillar', 'wow', 'thought alice', 'said alice')

    new_trie = make_word_trie(text)
    values = autocorrect(new_trie, 'hear', 12)
    print(values)

    count = 0
    for i in myTrie:
        count += 1
    print("There are this many distinct sentences in Alice in Wonderland: ")
    print(count)


    print("There are this many sentences in Alice in Wonderland: ")
    print(len(tokenize_sentences(text)))
    return None

def codeQuestion2():
    """
    prints out answers to the questions in the lab
    """
    with open("metamorphosis.txt", encoding="utf-8") as f:
        text = f.read()
    myTrie = make_word_trie(text)
    # answer = autocomplete(myTrie, 'gre', 6)
    # print(answer)
    # print(word_filter(myTrie, 'c*h'))
    printList = []
    for word in myTrie:
        if word[0][0] == 'c' and word[0][-1] == 'h':
            printList.append(word)
    print(printList)

    return None

def codeQuestion3():
    """
    prints out answers to the questions in the lab
    """
    with open("gutenberg.txt", encoding="utf-8") as f:
        text = f.read()
    myTrie = make_word_trie(text)
    count = 0
    for i in myTrie:
        count += 1
    print("In dracula, there are this many distinct words: ")
    print(count)

    sentences = tokenize_sentences(text)
    words = []
    for sentence in sentences:
        to_add = sentence.split()
        for word in to_add:
            words.append(word)
    print("In dracula, there are this many words: ")
    print(len(words))


def codeQuestion4():
    """
    prints out answers to the questions in the lab
    """
    with open("pridprejudice.txt", encoding="utf-8") as f:
        text = f.read()
    myTrie = make_word_trie(text)
    print(autocorrect(myTrie, 'hear', 500))

def codeQuestion5():
    """
    prints out answers to the questions in the lab
    """
    with open("twocities.txt", encoding="utf-8") as f:
        text = f.read()
    myTrie = make_word_trie(text)
    printList = []
    for word in myTrie:
        if word[0][0] == 'r' and word[0][-1] == 't' and word[0][2] == 'c':
            printList.append(word)
    print(printList)
# you can include test cases of your own in the block below.
if __name__ == "__main__":
    # test cases below were used in autocorrect
    # theTrie = make_word_trie('this is a long text where we want to create a word tree for all the words in this text I wanted to find wadner wanderer wandering wanderer wanderer wanker wanderingly')
    # print(autocorrect(theTrie, 'wander'))
    # print(autocorrect(theTrie, 'waneer'))
    # theTrie = make_word_trie("car cattle crate at at chat chat cat hat map set how to create")
    # print(autocorrect(theTrie, 'cat', 5))
    # codeQuestion1()

    # trie = make_word_trie("man mat mattress map me met a man a a a map man met")
    # result = word_filter(trie, '*?')
    # print(result)
    doctest.testmod()
