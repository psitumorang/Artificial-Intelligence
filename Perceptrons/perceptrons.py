############################################################
# Perceptrons
############################################################


############################################################
# Imports
############################################################

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
                keys = list(t[0].keys())
                yi = t[1]
                
                yi_pred = 0
                for key in keys:
                    w = 0
                    xi = t[0].get(key)
            
                    if self.w_dct.get(key) != None:
                        w = self.w_dct.get(key)

                    yi_pred += w * xi

                yi_pred = sign(yi_pred)

                #print(key, w * xi, yi, yi_pred, yi == yi_pred, yi < 0)
                if yi_pred != yi:
                    for key in keys:
                        w = 0
                        xi = t[0].get(key)

                        if self.w_dct.get(key) != None:
                            w = self.w_dct.get(key)

                        w = (w + xi) if yi ==True else (w - xi)
                        self.w_dct[key] = w
    

    def predict(self, x):
        prediction = 0
        for key in x.keys():
            xi = x.get(key)
            w = 0
            
            if self.w_dct.get(key) != None:
                w = self.w_dct.get(key)
            
            if isinstance(xi, float) or isinstance(xi, int):
                prediction += xi * w
        return sign(prediction)
    
    

class MulticlassPerceptron(object):

    def __init__(self, examples, iterations):
        self.w_dct = {}
        
        for t in examples:
            label = t[1]
            #if self.w_dct.get(label) == None:
            self.w_dct[label] = {}
                
        for i in range(iterations):
            for t in examples:
                # extract elements of t
                keys = tuple(list(t[0].keys()))
                yi = t[1]

                # set up the predictions dictionary
                yi_pred_dct = {}

                # dot product of wlk and xi
                for label in self.w_dct.keys():
                    yi_pred = 0
                    for key in keys:
                        w = 0
                        xi = t[0].get(key)

                        if self.w_dct[label].get(key) != None:
                            w = self.w_dct[label].get(key)

                        yi_pred += w * xi
                    yi_pred_dct[label] = yi_pred

                yi_pred = max(yi_pred_dct, key=yi_pred_dct.get)

                if yi != yi_pred:
                    for key in keys:
                        # increase true
                        w = 0
                        xi = t[0].get(key)

                        if self.w_dct[yi].get(key) != None:
                            w = self.w_dct[yi].get(key)

                        self.w_dct[yi][key] = w + xi

                        # decrease predicted
                        w = 0

                        if self.w_dct[yi_pred].get(key) != None:
                            w = self.w_dct[yi_pred].get(key)

                        self.w_dct[yi_pred][key] = w - xi
    
    def predict(self, x):
        yi_pred_dct = {}

        # dot product of wlk and xi
        for label in self.w_dct.keys():
            yi_pred = 0
            for key in x.keys():
                w = 0
                xi = x.get(key)

                if self.w_dct[label].get(key) != None:
                    w = self.w_dct[label].get(key)

                yi_pred += w * xi
            yi_pred_dct[label] = yi_pred

        yi_pred = max(yi_pred_dct, key=yi_pred_dct.get)
        return yi_pred

############################################################
# Section 2: Applications
############################################################

class IrisClassifier(object):

    def __init__(self, data):
        self.examples = []
        
        for i in data:
            features = i[0]
            label = i[1]
            dct = {}
            for j in range(len(features)):
                dct[j] = features[j]
            self.examples.append((dct, label))
        
        self.perceptron = MulticlassPerceptron(self.examples, 100)

    def classify(self, instance):
        instance_dct = {}
        for i in range(len(instance)):
            instance_dct[i] = instance[i]
        
        return self.perceptron.predict(instance_dct)

class DigitClassifier(object):

    def __init__(self, data):
        self.examples = ()
        
        for i in data:
            features = i[0]
            label = i[1]
            dct = {}
            for j in range(len(features)):
                dct[j] = features[j]
            self.examples = self.examples + ((dct, label), )
        
        self.perceptron = MulticlassPerceptron(self.examples, 11)

    def classify(self, instance):
        instance_dct = {}
        for i in range(len(instance)):
            instance_dct[i] = instance[i]
        
        return self.perceptron.predict(instance_dct)

class BiasClassifier(object):

    def __init__(self, data):
        self.examples = ()
        
        self.falses = ()
        self.trues = ()
        
        for i in data:
            if i[1] == False:
                self.falses = self.falses + ((i[0]),)
            else:
                self.trues = self.trues + ((i[0]),)
            
        self.bias = sum(self.trues)/len(self.trues) - sum(self.falses)/len(self.falses)
        
        for i in data:
            dct = {}
            dct["x1"] = i[0] 
            dct["x2"] = i[0] - self.bias
            
            self.examples = self.examples + ((dct, i[1]), )
        
        self.perceptron = BinaryPerceptron(self.examples, 200)

    def classify(self, instance):
        instance_dct = {}
        instance_dct["x1"] = instance
        instance_dct["x2"] = instance - self.bias

        return self.perceptron.predict(instance_dct)

class MysteryClassifier1(object):

    def __init__(self, data):
        self.examples = ()
            
        # calculate bias for first feature
        self.falses_0 = ()
        self.trues_0 = ()
        
        for i in data:
            if i[1] == False:
                self.falses_0 = self.falses_0 + ((i[0][0]),)
            else:
                self.trues_0 = self.trues_0 + ((i[0][0]),)
            
        self.bias_0 = sum(self.trues_0)/len(self.trues_0) - sum(self.falses_0)/len(self.falses_0)
        
        # calculate bias for second feature
        self.falses_1 = ()
        self.trues_1 = ()
        
        for i in data:
            if i[1] == False:
                self.falses_1 = self.falses_1 + ((i[0][1]),)
            else:
                self.trues_1 = self.trues_1 + ((i[0][1]),)
            
        self.bias_1 = sum(self.trues_1)/len(self.trues_1) - sum(self.falses_1)/len(self.falses_1)
        
        # train with two engineered features
        for i in data:
            features = i[0]
            label = i[1]
            dct = {}
            for j in range(len(features)):
                dct[j] = features[j]
            
            dct["bias_0"] = dct.get(0) - self.bias_0  
            dct["bias_1"] = dct.get(1) - self.bias_1 
            
            dct["squared_0"] = dct.get(0) ** 2
            dct["squared_1"] = dct.get(1) ** 2
            
            dct["cubed_0"] = dct.get(0) ** 3
            dct["cubed_1"] = dct.get(1) ** 3
            
            self.examples = self.examples + ((dct, label), )
        
        self.perceptron = BinaryPerceptron(self.examples, 100)
        
    def classify(self, instance):
        instance_dct = {}
        
        instance_dct[0] = instance[0]
        instance_dct[1] = instance[1]
        
        instance_dct["bias_0"] = instance[0] - self.bias_0  
        instance_dct["bias_1"] = instance[1] - self.bias_1 
        
        instance_dct["squared_0"] = instance[0] ** 2
        instance_dct["squared_1"] = instance[1] ** 2
            
        instance_dct["cubed_0"] = instance[0] ** 3
        instance_dct["cubed_1"] = instance[1] ** 3

        return self.perceptron.predict(instance_dct)

class MysteryClassifier2(object):

    def __init__(self, data):
        self.examples = ()
            
            
        # calculate bias for first feature
        self.falses_0 = ()
        self.trues_0 = ()
        
        for i in data:
            if i[1] == False:
                self.falses_0 = self.falses_0 + ((i[0][0]),)
            else:
                self.trues_0 = self.trues_0 + ((i[0][0]),)
            
        self.bias_0 = sum(self.trues_0)/len(self.trues_0) - sum(self.falses_0)/len(self.falses_0)
        
        # calculate bias for second feature
        self.falses_1 = ()
        self.trues_1 = ()
        
        for i in data:
            if i[1] == False:
                self.falses_1 = self.falses_1 + ((i[0][1]),)
            else:
                self.trues_1 = self.trues_1 + ((i[0][1]),)
            
        self.bias_1 = sum(self.trues_1)/len(self.trues_1) - sum(self.falses_1)/len(self.falses_1)
        
        # calculate bias for second feature
        self.falses_2 = ()
        self.trues_2 = ()
        
        for i in data:
            if i[1] == False:
                self.falses_2 = self.falses_2 + ((i[0][2]),)
            else:
                self.trues_2 = self.trues_2 + ((i[0][2]),)
            
        self.bias_2 = sum(self.trues_2)/len(self.trues_2) - sum(self.falses_2)/len(self.falses_2)
        
        # train with two engineered features
        for i in data:
            features = i[0]
            label = i[1]
            dct = {}
            
            new_feature = 0
            #neg
            if features[0] < 0 and features[1] < 0 and features[2] < 0:
                new_feature = -1
                
            if features[0] < 0 and features[1] > 0 and features[2] > 0:
                new_feature = -1
                
            if features[0] > 0 and features[1] < 0 and features[2] > 0:
                new_feature = -1
                
            if features[0] > 0 and features[1] > 0 and features[2] < 0:
                new_feature = -1
                
            # pos
            if features[0] < 0 and features[1] < 0 and features[2] > 0:
                new_feature = 1
                
            if features[0] < 0 and features[1] > 0 and features[2] < 0:
                new_feature = 1
                
            if features[0] > 0 and features[1] < 0 and features[2] < 0:
                new_feature = 1
                
            if features[0] > 0 and features[1] > 0 and features[2] > 0:
                new_feature = 1
                
            dct['new_feature'] = new_feature
            
            #for j in range(len(features)):
                #dct[j] = features[j]
            
            #dct["bias_0"] = dct.get(0) - self.bias_0  
            #dct["bias_1"] = dct.get(1) - self.bias_1 
            #dct["bias_2"] = dct.get(2) - self.bias_2 
            
            #dct["squared_0"] = dct.get(0) ** 2
            #dct["squared_1"] = dct.get(1) ** 2
            #dct["squared_2"] = dct.get(2) ** 2
            
            #dct["cubed_0"] = features[0] ** 3
            #dct["cubed_1"] = features[1] ** 3
            #dct["cubed_2"] = features[2] ** 3
            
            #dct["fifth_0"] = features[0] ** 5
            #dct["fifth_1"] = features[1] ** 5
            #dct["fifth_2"] = features[2] ** 5
            
            #dct["sum"] = features[0] + features[1] + features[2]
            #dct["sum_fifth"] = (features[0] + features[1] + features[2]) ** 5
            #dct["fourth_0"] = dct.get(0) ** 4
            #dct["fourth_1"] = dct.get(1) ** 4
            #dct["fourth_2"] = dct.get(2) ** 4
            
            #dct["fifth_0"] = dct.get(0) ** 5
            #dct["fifth_1"] = dct.get(1) ** 5
            #dct["fifth_2"] = dct.get(2) ** 5
            
            self.examples = self.examples + ((dct, label), )
        
        self.perceptron = BinaryPerceptron(self.examples, 500)
        
    def classify(self, instance):
        instance_dct = {}
        
        new_feature = 0
            #neg
        if instance[0] < 0 and instance[1] < 0 and instance[2] < 0:
            new_feature = -1

        if instance[0] < 0 and instance[1] > 0 and instance[2] > 0:
            new_feature = -1

        if instance[0] > 0 and instance[1] < 0 and instance[2] > 0:
            new_feature = -1

        if instance[0] > 0 and instance[1] > 0 and instance[2] < 0:
            new_feature = -1

        # pos
        if instance[0] < 0 and instance[1] < 0 and instance[2] > 0:
            new_feature = 1

        if instance[0] < 0 and instance[1] > 0 and instance[2] < 0:
            new_feature = 1

        if instance[0] > 0 and instance[1] < 0 and instance[2] < 0:
            new_feature = 1

        if instance[0] > 0 and instance[1] > 0 and instance[2] > 0:
            new_feature = 1
            
        instance_dct['new_feature'] = new_feature
        #instance_dct[0] = instance[0]
        #instance_dct[1] = instance[1]
        #instance_dct[2] = instance[2]
        
        #instance_dct["bias_0"] = instance[0] - self.bias_0  
        #instance_dct["bias_1"] = instance[1] - self.bias_1   
        #instance_dct["bias_2"] = instance[2] - self.bias_2 
        
        #instance_dct["squared_0"] = instance[0] ** 2
        #instance_dct["squared_1"] = instance[1] ** 2
        #instance_dct["squared_2"] = instance[2] ** 2
            
        #instance_dct["cubed_0"] = instance[0] ** 3
        #instance_dct["cubed_1"] = instance[1] ** 3
        #instance_dct["cubed_2"] = instance[2] ** 3
        
        #instance_dct["fifth_0"] = instance[0] ** 3
        #instance_dct["fifth_1"] = instance[1] ** 3
        #instance_dct["fifth_2"] = instance[2] ** 3
        
        #instance_dct["sum"] = instance[0] + instance[1] + instance[2]
        #instance_dct["sum_fifth"] = (instance[0] + instance[1] + instance[2]) ** 5
        
        #instance_dct["fourth_0"] = instance[0] ** 4
        #instance_dct["fourth_1"] = instance[1] ** 4
        #instance_dct["fourth_2"] = instance[2] ** 4
            
        #instance_dct["fifth_0"] = instance[0] ** 5
        #instance_dct["fifth_1"] = instance[1] ** 5
        #instance_dct["fifth_2"] = instance[2] ** 5

        return self.perceptron.predict(instance_dct)
