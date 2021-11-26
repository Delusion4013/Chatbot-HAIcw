import random
import json

import systems.game as game
import systems.information_retrieval as IR
import systems.small_talk as ST
import systems.identity_managment as IM


class Chatbot():

    user_responses = []     # user's response stack used to track context
                            # not implemented in this chatbot.
    current_response = ""   # The latest user's response

    # User profile
    user_name = []
    name_get = False
    
    # Bot profile
    robot_name = "Jarvis"

    # Constants for text matching
    IDENTITY_INPUTS = ()
    IDENTITY_FIRST_RESPONSES = ()
    IDENTITY_SECOND_RESPONSES = ()
    GOODBYE_RESPONSES = ()

    # Data path
    user_profile_path = "data/user_profile.json"

    def __init__(self, robot_name):
        # Keyword Matching
        self.IDENTITY_INPUTS = ("what is my name?", "who am i?","what is my name", "who am i")
        self.GOODBYE_RESPONSES = ("Bye! Take care.", "See you soon!", "Have a nice day!", "Enjoy your day!")
        self.robot_name = robot_name
        
    def init_profile(self):    
        with open(self.user_profile_path, 'r', encoding='utf8', errors='ignore') as fin:
            profile = json.load(fin)
            if profile['Name'] != "":
                self.user_name = profile['Name']
                self.name_get = True

    def show_menu(self):
        """
            Prompt the user with help information on the chatbot's capability.
        """
        print("1) if you want to ask questions, type [QA]")
        print("2) if you want to play games, type [games]")
        print("3) if you want to order something, type [transaction]")

    def robo_utter(self, utterance):
        """
            Customize chatbot's prompts by using pre-set robot name.
        """
        print(self.robot_name + ": " + utterance)

    def update_database(self):
        profile = {'Name': self.user_name}
        with open(self.user_profile_path, "w") as f:
            json.dump(profile, f, indent=4)
        return

    def goodbye(self):
        return random.choice(self.GOODBYE_RESPONSES)

    def intent_match(self, user_response):
        """
            Matches user's intent based on keywords and patterns. 
            Then invoke the relevant sub systems.
        """

        if (user_response == 'menu' or user_response == 'help'):
            self.show_menu()
        elif (user_response == 'qa' or user_response == 'IR'):
            IR.pipeline(self.robot_name)
        elif (user_response == 'games'):
            self.user_name = game.pipeline(self.user_name, self.robot_name)
            self.name_get = True
        elif (ST.pipeline(user_response) != None):
            self.robo_utter(ST.pipeline(user_response))
        elif (user_response =='thanks' or user_response == 'thank you'):
            self.robo_utter("You are welcome.")
        elif(user_response in self.IDENTITY_INPUTS):
            (self.user_name, self.name_get) = IM.pipeline(self.robot_name, self.user_name, self.name_get)
        else:
            self.robo_utter("I am sorry! I don't understand you.")
        return

    def general_pipeline(self):
        """
            The general procedure for chatbot taking in user input and generates response.
        """

        self.init_profile()
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

