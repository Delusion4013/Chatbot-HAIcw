from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import string
import csv
import warnings
import json
    
def LemTokens(tokens):
    """
        Customized pre-processor which use WordNetLemmatizer for lemmatization

        Used in LemNormalize() method
    """
    lemmer = WordNetLemmatizer()
    return [lemmer.lemmatize(token) for token in tokens]

def LemNormalize(text):
    """
        Customized lemmatizer for IR system which excludes punctuations in the input.

        Used in search() method for model creation.
    """
    remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

def preprocess(query):
    """
        A pipeline for pre-process user's input.

        The procedure are as follows: 
            1. Tokenize 
            2. POS tagging 
            3. Stemming/Lemmatization
            4. Stopwords filtering
    """
    tokenized_query = nltk.word_tokenize(query)
    tagged_response = nltk.pos_tag(tokenized_query, tagset="universal")
    lemmer = WordNetLemmatizer()
    Lemed_response = [lemmer.lemmatize(word) for word in tagged_response]
    tokens_without_sw = [word.lower() for word in Lemed_response if not word in stopwords.words()]
    return " ".join(tokens_without_sw)


def response(user_response):
    """
        Based on user's input query, prompt different info.
    """
    (idx, qs) = search(user_response)
    INTERROGATIVE_PRONOUN = ("what", "where", "when", "who", "why","how")
    robo_response = ''
    if(qs <= 0.2):
        robo_response = robo_response + "I am sorry! Nothing relevant found in my database."
        return robo_response
    else:
        if user_response.endswith('?') or user_response.startswith(INTERROGATIVE_PRONOUN):
            ans = parseAnswer(idx, True)
            robo_response = robo_response+ans
        else:
            ans = parseAnswer(idx, False)
            robo_response = robo_response+ans
        return robo_response

def search(query):
    """
        Perform search through the QA database based on query.
        During this method, a model of the database would be built.

        Returns:
            - The index of most relevant entriy
            - The similarity calculated
    """

    with open('data/qa.csv', 'r', encoding='utf8', errors='ignore') as database:
        reader = csv.reader(database)
        lines = [" ".join(row) for row in reader]
    
    lines.append(query)
    
    # Define TF-IDF weighted language model with WordNetLemmatizer
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    
    # Construct Tfidf Vectorizer
    tfidf = TfidfVec.fit_transform(lines)
    
    # Calculate the cosine similarity between user query and the qa databse
    vals = cosine_similarity(tfidf[-1], tfidf)
    
    # Get the index of QA entries that has the highest cosine similarity
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()

    # Get the cosine similarity
    query_similarity = flat[-2]
    lines.remove(query)
    return (idx, query_similarity)

def parseAnswer(index, is_question):
    """
        Based on query type, prompt different information.

        Returns: Parsed string for prompt.
    """
    database = {}
    with open("data/qa.json", "r") as f:
        database = json.load(f)
    # Reading in the corpus
    questions = database['Question']
    answers = database['Answer']
    if is_question:
        res = f"\nFounded the most relevant question in database.\n\nQ: {questions[index-1]}?\nA: {answers[index-1]}\n"
    else:
        res = f"\nFounded the most relevant information in database.\n\n{answers[index-1]}\n"
    return res

def pipeline(robot_name):
    """
        General procedure for this sub system.
    """
    warnings.filterwarnings('ignore')
    print(robot_name + ": Welcome to search questions. Just type your query in.")
    print(robot_name + ": If you are done, Type [Close] to exit.")
    flag = True
    while(flag == True):
        user_response = input("> ")
        user_response = user_response.lower()
        if (user_response != 'close'):
            print(robot_name + ': Searching.....')
            print(response(user_response))
        else:
            flag = False
            print(robot_name + ": Wish the information is helpful~")

# To test the sub system, invoke pipeline here
# pipeline("Jarvis")