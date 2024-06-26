############################################################
# Language Models
############################################################


############################################################
# Imports
############################################################


############################################################
# Section 1: Markov Models
############################################################

def tokenize(text):
    text = text.strip()
    punc = string.punctuation
    whitespaces = [" ", "\t", "\n", "\v", "\r", "\f"]
    
    tokens = []
    word = ""
    count = 0
    
    for i in text:
        count +=1
        if i in punc:
            if word!= "":
                tokens.append(word)
            tokens.append(i)
            
            word = ""
        elif i in whitespaces:
            if word!= "":
                tokens.append(word)
            word = ""
        else:
            word += str(i)
            if count == len(text):
                tokens.append(word)
            
    return tokens

def ngrams(n, tokens):     
    count = 0 
    ngrams = ()
    
    if n == 1:
        for token in tokens:
            ngrams = ngrams + (((),token),)
        ngrams = ngrams + (((), '<END>'),)
    else:
        for i in range(len(tokens) + 1):
            num_starts = n - 1 - count
            context = ()

            for j in range(num_starts):
                context = context + (('<START>'),)

            count2 = n - 1 - num_starts

            for k in range(count2):
                context = context + ((tokens[count- count2]),)
                count2 -= 1

            context = context[-(n-1):]

            ngram = None
            if count == len(tokens):
                ngram = (context, '<END>')
            else:
                ngram = (context, tokens[count])

            ngrams = ngrams + ((ngram),)
            count += 1

    return list(ngrams)

class NgramModel(object):

    def __init__(self, n):
        self.n = n
        self.ngrams_dct = {}

    def update(self, sentence):
        ngrams_lst = ngrams(self.n, tokenize(sentence))
        for ngram in ngrams_lst:
            if self.ngrams_dct.get(ngram[0]) == None:
                self.ngrams_dct[ngram[0]] = [ngram[1]]
            else:
                self.ngrams_dct[ngram[0]] += [ngram[1]]

    def prob(self, context, token):
        denominator = len(self.ngrams_dct.get(context))
        numerator = self.ngrams_dct.get(context).count(token)
        
        if self.ngrams_dct.get(context) == None:
            return 0
        else:
            return numerator / denominator

    def random_token(self, context):
        r = random.random()
        
        distribution = self.ngrams_dct.get(context)
        token_set = sorted(set(distribution))
        
        prob_dst = {}
        for token in token_set:
            prob_dst[token] = distribution.count(token) / len(distribution)
        
        cumulative_pr = 0
        
        for token in token_set:
            if cumulative_pr <= r and r < cumulative_pr + prob_dst[token]:
                #print('r:' + str(r), ', cumulative_pr:' + str(cumulative_pr), ' dist:' + str(distribution[i]), 'i:' + str(i))
                return token
            
            cumulative_pr += prob_dst[token]

    def random_text(self, token_count):
        text = ""
        context = ['<START>' for i in range(self.n - 1)]
    
        for i in range(token_count):
            word = self.random_token(tuple(context))
            text = text + word + " "

            if word == '<END>':
                context = ['<START>' for i in range(self.n - 1)]
            else:
                context.append(word)
                context.pop(0)
            
        return text.strip()

    def perplexity(self, sentence):
        ngrams_lst = ngrams(self.n, tokenize(sentence))
        
        ps = ()
        for ngram in ngrams_lst:
            p = self.prob(ngram[0], ngram[1])
            ps = ps + ((p),)
        
        prod_ps = 1
        for p in ps:
            prod_ps = prod_ps * p
    
        return (1/prod_ps) ** (1/len(ngrams_lst))

def create_ngram_model(n, path):
    txt = open(path).readlines()
    
    m = NgramModel(n)
    for line in txt:
        m.update(line)
    
    return m

