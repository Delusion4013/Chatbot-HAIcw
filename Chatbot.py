import random
import nltk
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk.tree import Tree;

import systems.game as game
import systems.information_retrieval as IR


class Chatbot():

    user_responses = []
    current_response = []

    # User profile
    user_name = []
    name_get = False
    robot_name = "Jarvis"

    # Constants for text matching
    GREETING_INPUTS = ()
    GREETING_RESPONSES = ()
    NAME_INPUTS = ()
    IDENTITY_INPUTS = ()
    IDENTITY_FIRST_RESPONSES = ()
    IDENTITY_SECOND_RESPONSES = ()
    GOODBYE_RESPONSES = ()

    # Data path
    user_profile_path = "data/user_profile.txt"

    def __init__(self):
        print("Robo: Hi! This is Robo, how can I help you?")

        # Keyword Matching
        self.GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey","good morning","good afternoon","good evening")
        self.GREETING_RESPONSES = ("Hi", "Hey", "*nods*", "Hi there", "Hello","Greetings", "I am glad to meet you", "")
        self.NAME_INPUTS = ("my name is", "i am", "call me", "i'm")
        self.IDENTITY_FIRST_RESPONSES = ("I will remember you ", "I will keep it in my database ", "Got you! ")
        self.IDENTITY_SECOND_RESPONSES = ("I remember you, you are ", "I find it in my database, ", "Nice seeing you again! ")
        self.IDENTITY_INPUTS = ("what is my name?", "who am i")
        self.GOODBYE_RESPONSES = ("Bye! Take care.", "See you soon!", "Have a nice day!", "Enjoy your day!")

    def greeting(self, sentence):
        # Intent matching done by text matching
        for word in sentence.split():
            if word.lower() in self.GREETING_INPUTS:
                return random.choice(self.GREETING_RESPONSES)

    def goodbye(self):
        return random.choice(self.GOODBYE_RESPONSES)

    def identity(self, sentence):
        words = word_tokenize(sentence)
        # print(words)
        tokens_without_sw = [word.title() for word in words
                                if word not in stopwords.words()] # stop words removal
        # print(tokens_without_sw)
        postags = pos_tag(tokens_without_sw)
        word_tags = nltk.ne_chunk(postags, binary=False)
        for tag in word_tags:
            if type(tag) == Tree and tag.label() == 'PERSON':
                for item in tag:
                    self.user_name.append(item[0] + '')
        print(self.user_name)

        if self.user_name:
            self.name_get = True
        if self.name_get:
            print(type(self.user_name))
            self.user_name = ' '.join(self.user_name)
            print("ROBO: " + random.choice(self.IDENTITY_FIRST_RESPONSES) + self.user_name)

    def general_pipeline(self):
        # Propose welcome information
        flag = True
        while(flag == True): 
            # Wait for user input
            user_response = input("YOU: ")
            user_response = user_response.lower()
            # Intent matching
            if(user_response !='bye'):
                if (user_response =='thanks' or user_response == 'thank you'):
                    flag == False
                    print("ROBO: You are welcome.")
                elif (user_response == 'menu' or user_response == 'help'):
                    self.show_menu()
                elif (user_response == 'qa'):
                    # information retriviel
                    IR.pipeline()
                elif (user_response == 'games'):
                    self.user_name = game.pipeline(self.user_name, self.robot_name)
                    self.name_get = True
                elif (user_response == 'small talk'):
                    # start small talk
                    print('Small talk')
                elif (user_response == 'transaction'):
                    # transaction system
                    print('transaction system')
                elif(self.greeting(user_response)!=None):
                    print("ROBO: "+ self.greeting(user_response))
                elif(user_response in self.IDENTITY_INPUTS):
                    if self.name_get == True:
                        print("ROBO: " + random.choice(self.IDENTITY_SECOND_RESPONSES) + self.user_name)
                    elif self.name_get == False:
                        print("ROBO: You didn't tell me your name! Please tell me and I will keep it down.")
                        user_response = input("YOU: ")
                        self.identity(user_response)
                else:
                    # print(self.retrieveInfo(user_response))
                    print("ROBO: I am sorry! I don't understand you")
            else:
                flag = False
                print("ROBO: " + self.goodbye())
                self.update_data()
        return

    def show_menu(self):
        print("1) if you want to ask questions, type [QA]")
        print("2) if you want to play games, type [games]")
        print("3) if you want to do some small talks, type [small talk]")
        print("4) if you want to order something, type [transaction]")

    def intent_match(self, current_response):
        # print(current_response)
        return

    def update_database(self):
        # if (self.)
        # open(self.user_profile_path, 'rw')
        return

