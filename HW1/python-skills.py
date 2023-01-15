############################################################
# CIS 521: Python Skills Homework
############################################################

student_name = "Philip Situmorang"

# This is where your grade report will be sent.
student_email = "pslatte@seas.upenn.edu" 

############################################################
# Section 1: Python Concepts
############################################################

python_concepts_question_1 = "..."

python_concepts_question_2 = "..."

python_concepts_question_3 = "..."

############################################################
# Section 2: Working with Lists
############################################################

def extract_and_apply(l, p, f):
    return [f(x) for x in l if p(x)]

def concatenate(seqs):
    return [x for item in seqs for x in item]

def transpose(matrix):
    num_new_columns = len(matrix)
    num_new_rows = len(matrix[0])
    new_matrix = []
    
    # create new empty matrix, using 0 as filler
    for row in range(num_new_rows):
        new_row = []
        for column in range(num_new_columns):
            new_row.append(0)
        new_matrix.append(new_row)
    
    # the transposed matrix
    i = 0
    for row in matrix:
        j = 0
        for x in row:
            new_matrix[j][i] = x
            j +=1
        i+=1
    
    return new_matrix

############################################################
# Section 3: Sequence Slicing
############################################################

def copy(seq):
    new_seq = seq
    return new_seq

def all_but_last(seq):
    new_seq = seq
    if len(seq) != 0:
        new_seq = seq[:-1]
    return new_seq

def every_other(seq):
    return seq[::2]

############################################################
# Section 4: Combinatorial Algorithms
############################################################

def prefixes(seq):
    seqlen = len(seq)
    i = 0
    while i < seqlen + 1:
        yield seq[:i]
        i += 1

def suffixes(seq):
    seqlen = len(seq)
    i = 0
    lst = []
    while i < seqlen + 1:
        yield seq[i:]
        i += 1

def slices(seq):
    seqlen = len(seq)
    i = 0
    j = 0
    while j < seqlen + 1:
        if len(seq[j:i]) != 0:
            yield seq[j:i]
        i += 1
        if i == seqlen + 1:
            i = 0
            j += 1

############################################################
# Section 5: Text Processing
############################################################

def normalize(text):
    wordlst = text.lower().split()
    newtext = ' '.join(word for word in wordlst)
    return newtext

def no_vowels(text):
    newtext = text
    for character in 'aeiou':
        newtext = newtext.replace(character,'')
    return newtext

def digits_to_words(text):
    nums = {'1':'one',
            '2':'two',
            '3':'three',
            '4':'four',
            '5':'five',
            '6':'six',
            '7':'seven',
            '8':'eight',
            '9':'nine'}
    numlst = []
    for i in text:
        if nums.get(i) is not None:
            numlst.append(nums.get(i))
    return ' '.join(numlst)

def to_mixed_case(name):
    wordlst = name.lower().replace('_', ' ').split()
    for i in range(len(wordlst)):
        if i > 0:
            wordlst[i] = wordlst[i].capitalize()
    return ''.join(wordlst)

############################################################
# Section 6: Polynomials
############################################################

class Polynomial(object):

    def __init__(self, polynomial):
        self.polynomial = tuple(polynomial)

    def get_polynomial(self):
        return self.polynomial

    def __neg__(self):
        lst = list(self.polynomial)
        for i in range(len(lst)):
            lst[i] = list(lst[i])
            lst[i][0] = -lst[i][0]
            lst[i] = tuple(lst[i])
        return Polynomial(tuple(lst))

    def __add__(self, other):
        lst1 = list(self.polynomial)
        lst2 = list(other.polynomial)
        lst3 = lst1 + lst2
        return Polynomial(tuple(lst3))

    def __sub__(self, other):
        lst1 = list(self.polynomial)
        lst2 = list(other.polynomial)
        
        for i in range(len(lst2)):
            lst2[i] = list(lst2[i])
            lst2[i][0] = -lst2[i][0]
            lst2[i] = tuple(lst2[i])
            
        lst3 = lst1 + lst2
        return Polynomial(tuple(lst3))
    
    def __mul__(self, other):
        lst1 = list(self.polynomial)
        lst2 = list(other.polynomial)
        
        lst3 = []
        for i in lst1:
            for j in lst2:
                i = list(i)
                j = list(j)
                product = [i[0] * j[0], i[1] + j[1]]
                lst3.append(tuple(product))
        return Polynomial(tuple(lst3))

    def __call__(self, x):
        lst = list(self.polynomial)
        result = 0
        for i in range(len(lst)):
            lst[i] = list(lst[i])
            result += lst[i][0] * (x ** lst[i][1])
        return result

    def simplify(self):
        lst = list(self.polynomial)
        dct = {}
        for i in range(len(lst)):
            lst[i] = list(lst[i])
            if dct.get(lst[i][1]) is None:
                dct[lst[i][1]] = lst[i][0]
            else:
                dct[lst[i][1]] = dct.get(lst[i][1]) + lst[i][0]

        result = []
        for j in dct:
            if dct[j] != 0:
                result.append((dct[j], j))
            
        if len(result) == 0:
            result = [(0,0)]
                
        self.polynomial = tuple(result)

    def __str__(self):
        lst = list(self.polynomial)

        result = ''
        for i in range(len(lst)):
            lst[i] = list(lst[i])
            term = ''
    
            if lst[i][1] == 0:
                term = str(lst[i][0])
            elif lst[i][1] == 1:
                term = str(lst[i][0]) + 'x'
            else:
                term = str(lst[i][0]) + 'x^' + str(lst[i][1])
    
            if lst[i][0] == 1: 
                if lst[i][1] == 0:
                    term = '1'
                else:
                    term = term[1:]
            elif lst[i][0] == -1:
                if lst[i][1] == 0:
                    term = '-1'
                else:
                    term = '-' + term[2:]
    
            if i == 0:
                result = term
            else:
                if lst[i][0] < 0: 
                    term = term[1:]
                    result = result + ' - ' + term
                else:
                    result = result + ' + ' + term
        return result

############################################################
# Section 7: Python Packages
############################################################
import numpy as np
def sort_array(list_of_matrices):
    lst1 = []
    for matrix in list_of_matrices:
        lst1.append(list(matrix.flatten()))

    lst2 = []
    for i in lst1:
        lst2 = lst2 + i

    lst2 = np.sort(lst2)[::-1]
    return lst2

import nltk
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
def POS_tag(sentence):
    sentence = sentence.lower()
    tokens = word_tokenize(sentence)

    all_stopwords = stopwords.words('english')
    tokens_without_sw = [word for word in tokens if word not in all_stopwords]

    tokens_without_p = [word for word in tokens_without_sw if word not in string.punctuation]
    tags = nltk.pos_tag(tokens_without_p)
    return tags

############################################################
# Section 8: Feedback
############################################################

feedback_question_1 = """
About 6 hrs.
"""

feedback_question_2 = """
The polynomials were challenging. Haven't done oop in a while so switching
to that paradigm took awhile to adjust.
"""

feedback_question_3 = """
Python classes and oop. So far only done it in Java so it was good to learn how things
work in python.
"""