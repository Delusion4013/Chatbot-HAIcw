class Chatbot():

    user_responses = []
    current_response = []

    def __init__(self):
        print("ROBOT_NAME: Hi! This is Robert, how can I help you?")

    # def user_input(self):
    #     self.current_response = input("YOU:   ")
    #     print(self.user_response)

    def general_pipeline(self):
        # Propose welcome information
        # Wait for user input
        current_response = input("YOU:        ")
        # self.user_responses.append(self.current_response)
        while current_response != "Bye":
            contenet = self.preprocess(current_response)
            # intent = IntentClassifier.classify(content)
                # intent = self.intent_match(self.current_response)
            # subSystem = self.invoke(intent)
            # print(subSystem.generate_response())
            current_response = input("YOU:        ")
        return

    def intent_match(self, current_response):
        # print(current_response)
        

        return

    def preprocess(self, response):
        # print("Preprocessing " + response)

        # Pipeline: Tokenize -> POS tagging -> Stemming/Lemmatization -> Stopwords filtering

        # Tokenize
        import nltk
        from nltk.corpus import stopwords
        from nltk.tokenize import word_tokenize

        text_tokens = word_tokenize(response)
        tokens_without_sw = [word.lower() for word in text_tokens if not word in stopwords.words()]
        print(tokens_without_sw)
        filtered_sentence = (" ").join(tokens_without_sw)
        print(filtered_sentence)

        # Stemming

        # Lemmatization

        return ""


    # def invoke(self, intent):
    #     switch(intent):
    #         case "Identity":
                
    #         default:
    #             return SmallTalkGenerator()

    
