from os import remove
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.stem import WordNetLemmatizer
import string
import csv
import warnings
import json
warnings.filterwarnings('ignore')
    
# Preprocessing
def LemTokens(tokens):
    lemmer = WordNetLemmatizer()
    return [lemmer.lemmatize(token) for token in tokens]

def LemNormalize(text):
    remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

# Generating response
def response(user_response):

    with open('data/qa.csv', 'r', encoding='utf8', errors='ignore') as fin:
        reader = csv.reader(fin)
        lines = [" ".join(row) for row in reader]
    
    lines.append(user_response)

    # Define TF-IDF weighted language model with WordNetLemmatizer
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    # Construct Tfidf Vectorizer
    tfidf = TfidfVec.fit_transform(lines)
    # print(tfidf.toarray())

    # Calculate the cosine similarity between user query and the qa databse
    vals = cosine_similarity(tfidf[-1], tfidf)
    
    # Get the index of QA entries that has the highest cosine similarity
    idx = vals.argsort()[0][-2]

    flat = vals.flatten()
    flat.sort()

    # Get the cosine similarity
    req_tfidf = flat[-2]
    lines.remove(user_response)

    robo_response = 'ROBO: '
    if(req_tfidf == 0):
        robo_response = robo_response + "I am sorry! Nothing relevant found in my database."
        return robo_response
    else:
        ans = parseAnswer(idx)
        robo_response = robo_response+ans
        return robo_response

def parseAnswer(idx):
    database = {}
    with open("data/qa.json", "r") as f:
        database = json.load(f)
    # Reading in the corpus
    questions = database['Question']
    answers = database['Answer']
    return f"Founded the most relevant question in database.\n\nQ: {questions[idx-1]}?\nA: {answers[idx-1]}\n"

def pipeline():
    print("ROBO: Welcome to search informations. Just type your question in.")
    print("ROBO: Type [Bye] to exit.")
    flag = True
    while(flag == True):
        user_response = input("You: ")
        user_response = user_response.lower()
        if (user_response != 'bye'):
            print(response(user_response))
        else:
            flag = False
            print("ROBO: Wish the information is helpful~")

