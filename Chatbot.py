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
        self.current_response = input("YOU:   ")
        while self.current_response != "Bye":
            # intent = self.intent_match(self.current_response)
            # subSystem = self.invoke(intent)
            # print(subSystem.generate_response())
            self.current_response = input("YOU:   ")
        return

    def intent_match(self, current_response):
        print(current_response)
        return

    

bot = Chatbot()
bot.general_pipeline()