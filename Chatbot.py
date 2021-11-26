import random
import nltk
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk.tree import Tree;

import systems.game as game
import systems.information_retrieval as IR
import systems.small_talk as ST


class Chatbot():

    user_responses = []     # user's response stack used to track context
                            # not implemented in this chatbot.
    current_response = ""   # The latest user's response

    # User profile
    user_name = []
    name_get = False
    
    # Bot profile
    robot_name = "ROBO"

    # Constants for text matching
    NAME_INPUTS = ()
    IDENTITY_INPUTS = ()
    IDENTITY_FIRST_RESPONSES = ()
    IDENTITY_SECOND_RESPONSES = ()
    GOODBYE_RESPONSES = ()

    # Data path
    user_profile_path = "data/user_profile.txt"

    def __init__(self, robot_name):
        # Keyword Matching
        self.NAME_INPUTS = ("my name is", "i am", "call me", "i'm")
        self.IDENTITY_FIRST_RESPONSES = ("I will remember you ", "I will keep it in my database ", "Got you! ")
        self.IDENTITY_SECOND_RESPONSES = ("I remember you, you are ", "I find it in my database, ", "Nice seeing you again! ")
        self.IDENTITY_INPUTS = ("what is my name?", "who am i")
        self.GOODBYE_RESPONSES = ("Bye! Take care.", "See you soon!", "Have a nice day!", "Enjoy your day!")
        self.robot_name = robot_name

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
        print(self.robot_name + ": Hi! This is " + self.robot_name + ", how can I help you?")

        flag = True
        while(flag == True): 
            # Wait for user input
            user_response = input("YOU: ")
            user_response = user_response.lower()
            # Intent matching
            if(user_response !='bye'):
                self.intent_match(user_response)
            else:
                flag = False
                self.robo_utter(self.goodbye())
                self.update_database()
        return

    def show_menu(self):
        print("1) if you want to ask questions, type [QA]")
        print("2) if you want to play games, type [games]")
        print("3) if you want to do some small talks, type [small talk]")
        print("4) if you want to order something, type [transaction]")

    def intent_match(self, user_response):
        """
            Matches user's intent based on keywords and patterns. 
            Then invoke the relevant sub systems.
        """

        if (user_response == 'menu' or user_response == 'help'):
            self.show_menu()
        elif (user_response == 'qa' or user_response == 'IR'):
            IR.pipeline()
        elif (user_response == 'games'):
            self.user_name = game.pipeline(self.user_name, self.robot_name)
            self.name_get = True
        # elif (user_response == 'transaction'):
        #     # transaction system
        #     print('transaction system')
        elif (ST.pipeline(user_response) != None):
            self.robo_utter(ST.pipeline(user_response))
        elif (user_response =='thanks' or user_response == 'thank you'):
            print("ROBO: You are welcome.")
        elif(user_response in self.IDENTITY_INPUTS):
            if self.name_get == True:
                self.robo_utter(random.choice(self.IDENTITY_SECOND_RESPONSES) + self.user_name)
            elif self.name_get == False:
                self.robo_utter("You didn't tell me your name! Please tell me and I will keep it down.")
                user_response = input("YOU: ")
                self.identity(user_response)
        else:
            self.robo_utter("I am sorry! I don't understand you.")
        return

    def robo_utter(self, utterance):
        """
            Customize chatbot's prompts by using pre-set robot name.
        """
        print(self.robot_name + ": " + utterance)

    def update_database(self):
        # if (self.)
        # open(self.user_profile_path, 'rw')
        return

