############################################################
# CIS 521: Perceptrons Homework
############################################################

student_name = "Philip Situmorang"

############################################################
# Imports
############################################################

import perceptrons_data as data

# Include your imports here, if any are used.



############################################################
# Section 1: Perceptrons
############################################################
def sign(x):
    return True if x > 0 else False

class BinaryPerceptron(object):

    def __init__(self, examples, iterations):
        self.iterations = iterations
        self.w_dct = {}
        
        for i in range(iterations):
            for t in examples:
                w = 0
                key = list(t[0].keys())[0]
                xi = t[0].get(key)
                yi = t[1]

                if self.w_dct.get(key) != None:
                    w = self.w_dct.get(key)

                yi_pred = sign(w * xi)
                if yi_pred != yi:
                    w = (w + xi) if yi > 0 else (w - xi)
                    self.w_dct[key] = w
    

    def predict(self, x):
        prediction = 0
        for key in x.keys():
            xi = x.get(key)
            prediction += xi * self.w_dct.get(key)
        return sign(prediction)
    
    

class MulticlassPerceptron(object):

    def __init__(self, examples, iterations):
        pass
    
    def predict(self, x):
        pass

############################################################
# Section 2: Applications
############################################################

class IrisClassifier(object):

    def __init__(self, data):
        pass

    def classify(self, instance):
        pass

class DigitClassifier(object):

    def __init__(self, data):
        pass

    def classify(self, instance):
        pass

class BiasClassifier(object):

    def __init__(self, data):
        pass

    def classify(self, instance):
        pass

class MysteryClassifier1(object):

    def __init__(self, data):
        pass

    def classify(self, instance):
        pass

class MysteryClassifier2(object):

    def __init__(self, data):
        pass

    def classify(self, instance):
        pass

############################################################
# Section 3: Feedback
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
