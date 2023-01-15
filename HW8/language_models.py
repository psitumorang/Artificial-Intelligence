############################################################
# CIS 521: Language Models Homework 
############################################################

student_name = "Type your full name here."

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import string


############################################################
# Section 1: Markov Models
############################################################

def tokenize(text):
    text = text.strip()
    punc = string.punctuation
    
    tokens = []
    word = ""
    for i in text:
        if i in punc:
            tokens.append(i)
            if word!= "":
                tokens.append(word)
            word = ""
        elif i == " ":
            if word!= "":
                tokens.append(word)
            word = ""
        else:
            word +=i
            
    return tokens

def ngrams(n, tokens):
    pass

class NgramModel(object):

    def __init__(self, n):
        pass

    def update(self, sentence):
        pass

    def prob(self, context, token):
        pass

    def random_token(self, context):
        pass

    def random_text(self, token_count):
        pass

    def perplexity(self, sentence):
        pass

def create_ngram_model(n, path):
    pass

############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = 0

feedback_question_2 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""

feedback_question_3 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""
