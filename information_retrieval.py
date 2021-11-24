from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.stem import WordNetLemmatizer
import string
import csv
import warnings
# warnings.filterwarnings('ignore')

# Reading in the corpus
questions = []
answers = []
qas = []

with open('data/qa.csv', 'r', encoding='utf8', errors='ignore') as fin:
    raw = fin.read().lower()

# Tokenisation
sent_tokens = nltk.sent_tokenize(raw)
word_tokens = nltk.word_tokenize(raw)

# Preprocessing
lemmer = WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

# Generating response
def response(user_response):
    robo_response = ''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf == 0):
        robo_response = robo_response + "I am sorry!"
        return robo_response
    else:
        print(type(sent_tokens[idx]))
        # print(sent_tokens[idx].split(','))
        robo_response = robo_response+sent_tokens[idx]
        return robo_response

flag = True
while(flag == True):
    user_response = input()
    user_response = user_response.lower()
    if (user_response != 'bye'):
        print(response(user_response))
        sent_tokens.remove(user_response)
    else:
        flag = False
        print("Bye")

