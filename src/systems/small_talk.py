import random
import string

def preprocess(user_input):
    """
        Preprocess for small talk system. Remove all puncatuations in the input text.

        Returns: user input without punctuations.
    """
    remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
    return user_input.translate(remove_punct_dict)


def greeting(sentence):
    """
        Used templates to match user's greeting intents.

        Returns: randomly selected greeting response, none if user is not greeting.
    """
    # Intent matching done by text matching
    GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey","good morning","good afternoon","good evening")
    GREETING_RESPONSES = ("Hi", "Hey", "*nods*", "Hi there", "Hello","Greetings", "I am glad to meet you")
    if sentence.lower() in GREETING_INPUTS:
        return random.choice(GREETING_RESPONSES)
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

def weather(sentence):
    """
        Used templates to match user's weather checking intents.

        Returns: randomly selected response, none if user is not asking about weather.
    """
    WEATHER_INPUTS = ("what's the weather", "how's the weather", "tell me about weather", "weather")
    # Could use outer api
    WEATHER_RESPONSES = ("I guess it's sunny","How pity, it is a rainy day.", "A cloudy day.", "Why not go out and check?")
    if sentence.lower() in WEATHER_INPUTS:
        return random.choice(WEATHER_RESPONSES)

    for word in sentence.split():
        if word.lower() in WEATHER_INPUTS:
            return random.choice(WEATHER_RESPONSES)

def care(sentence):
    """
        Used templates to match user's small intents.

        Returns: randomly selected response, none if user shows no intent in caring.
    """
    CARE_INPUT = ("how are you", "everything ok", "how's everything going")
    CARE_RESPONSES = ("I am fine, thank you :)", "Just so so.")
    if sentence.lower() in CARE_INPUT:
        return random.choice(CARE_RESPONSES)


def pipeline(user_response):
    """
        Procedure for small talk system to handle user input.

        Returns: robot's response for deduced intents.
    """
    processed_input = preprocess(user_response)
    # print(processed_input)
    robo_greet = greeting(processed_input)
    robo_weather = weather(processed_input)
    robo_care = care(processed_input)
    if robo_greet != None:
        return robo_greet
    elif robo_weather != None:
        return robo_weather
    elif robo_care != None:
        return robo_care
    else:
        return