import random;


class Chatbot():

    user_responses = []
    current_response = []

    # User profile
    user = {}

    # Constants for text matching
    GREETING_INPUTS = ()
    GREETING_RESPONSES = ()
    NAME_INPUTS = ()
    IDENTITY_RESPONSES = ()

    # Data path
    user_profile_path = "data/user_profile.txt"

    def __init__(self):
        print("Robo: Hi! This is Robo, how can I help you?")
        # Keyword Matching
        self.GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey","good morning","good afternoon","good evening")
        self.GREETING_RESPONSES = ("Hi", "Hey", "*nods*", "Hi there", "hello","Greetings", "I am glad! You are talking to me")
        self.NAME_INPUTS = ("my name is", "i am", "call me", "i'm")
        self.IDENTITY_RESPONSES = ("I will remember you.", "I will keep it in my databse.", "Got you!")


    def greeting(self, sentence):
        # Intent matching done by text matching
        for word in sentence.split():
            if word.lower() in self.GREETING_INPUTS:
                return random.choice(self.GREETING_RESPONSES)

    def identity(self, sentence):
        for entry in self.NAME_INPUTS:
            if sentence.find(entry) != -1:
                temp_list = sentence.strip().split(entry)
                for sub in temp_list:
                    if sub == '':
                        continue;
                    else:
                        self.user['name'] = sub.title()
                        # print(self.user['name'])
                return random.choice(self.IDENTITY_RESPONSES)


    def general_pipeline(self):
        # Propose welcome information
        # Wait for user input
        # self.user_responses.append(self.current_response)
        flag = True
        while(flag == True): 
            user_response = input("YOU: ")
            user_response = user_response.lower()
            if(user_response !='bye'):
                if (user_response =='thanks' or user_response == 'thank you'):
                    flag == False;
                    print("ROBO: You are welcome.")
                else:
                    # Add other subsystem here
                    if(self.greeting(user_response)!=None):
                        print("ROBO: "+ self.greeting(user_response))

                    elif(self.identity(user_response)!=None):
                        print("ROBO: "+ self.identity(user_response))

                    else:
                        print("ROBO: I am sorry! I don't understand you")
            else:
                flag = False
                print("ROBO: Bye! tack care.")
                self.update_data()
            
            # content = self.preprocess(user_response)
            # intent = IntentClassifier.classify(content)
                # intent = self.intent_match(self.user_response)
            # subSystem = self.invoke(intent)
            # print(subSystem.generate_response())
            # user_response = input("YOU:        ")
        return

    def intent_match(self, current_response):
        # print(current_response)
        

        return

    def update_data(self):
        # if (self.)
        # open(self.user_profile_path, 'rw')


    def preprocess(self, response):
        # print("Preprocessing " + response)

        # Pipeline: Tokenize -> POS tagging -> Stemming/Lemmatization -> Stopwords filtering

        # Tokenize
        import nltk
        from nltk.tokenize import word_tokenize

        tokenized_response = word_tokenize(response)

        # POS tagging

        tagged_response = nltk.pos_tag(tokenized_response, tagset="universal")

        posmap = {
            'ADJ': 'j',
            'ADV': 'r',
            'NOUN': 'n',
            'VERB': 'v'
        }

        # Stemming


        # Lemmatization


        # Stopwords filtering
        from nltk.corpus import stopwords
        tokens_without_sw = [word.lower() for word in tokenized_response if not word in stopwords.words()]
        print(tokens_without_sw)
        
        filtered_sentence = (" ").join(tokens_without_sw)
        print(filtered_sentence)

        
        return ""


    # def invoke(self, intent):
    #     switch(intent):
    #         case "Identity":
                
    #         default:
    #             return SmallTalkGenerator()

    
