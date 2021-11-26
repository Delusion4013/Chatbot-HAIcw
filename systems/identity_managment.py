from os import name
import random
import nltk
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk.tree import Tree;


def identity(sentence):
    """
        Inspect a sentence to see if a name entity contains.

        Returns: a tuple with 
                    - the acquired user name
                    - a boolean variable indicating whether a name was found
    """
    user_name = []
    name_get = False

    words = word_tokenize(sentence)
    tokens_without_sw = [word.title() for word in words
                            if word not in stopwords.words()] # stop words removal
    postags = pos_tag(tokens_without_sw)
    
    # Use chunking mechanism to find names
    word_tags = nltk.ne_chunk(postags, binary=False)
    for tag in word_tags:
        if type(tag) == Tree and tag.label() == 'PERSON':
            for item in tag:
                user_name.append(item[0] + '')

    if user_name:
        name_get = True
    if name_get:
        user_name = ' '.join(user_name)
        return (user_name, name_get)
    
    return ("", name_get)

def pipeline(robot_name, userName, nameGet):
    """
        General procedure for this sub system.

        The input variables are:
            - robot_name: currently operating chatbot's name
            - userName: previously stored name, "" by default
            - nameGet: boolean variable indicating whether user name have been acquired.
    """

    IDENTITY_FIRST_RESPONSES = ("I will remember you ", "I will keep it in my database ", "Got you! ")
    IDENTITY_SECOND_RESPONSES = ("I remember you, you are ", "I find it in my database, ", "Nice seeing you again! ", "I know, ")
    name_get = nameGet
    user_name = userName

    # If the name was stored beforehand
    if name_get == True:
        print(robot_name + ": " + random.choice(IDENTITY_SECOND_RESPONSES) + user_name)
    else:
        # Obtain the name using identity() method.
        print(robot_name + ": You didn't tell me your name! Please tell me and I will keep it down.")
        # Using the while loop to enable users to re-enter.
        while name_get == False:
            user_response = input("> ")
            if user_response == "quit" or user_response == "q":
                break
            (user_name, name_get) = identity(user_response)
            if name_get == True:
                print(robot_name + ": " + random.choice(IDENTITY_FIRST_RESPONSES) + user_name)
                break
            else:
                print(robot_name + ": " + "No name detected in former input. Please try again...")
                print(robot_name + ": " + "Type [quit] to terminate this process.")
    return (user_name, name_get)

# To test the sub system, invoke pipeline here
# pipeline("Jarvis", "Chenkai Hu", True)
# pipeline("Jarvis", "", False)