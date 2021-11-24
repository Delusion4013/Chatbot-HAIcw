import json
import random

def text_quiz(user_name):
    # https://www.derekshidler.com/how-to-create-a-text-based-adventure-and-quiz-game-in-python/
    import time

    TRUE_RESPONSE = ["t", "true", "yes", "y"]
    FALSE_RESPONSE = ["f", "false","no", "n"]


    print ("ROBO: Remember, the following answers are only True or False.")
    print ("Evaluating your intelligence level...")
    time.sleep(0.5)
    print ("Searching database for quiz problems...")
    time.sleep(2)
    
    # Load questions from the database
    with open('data/game_data.json', "r") as quiz_dataset:
        quiz = json.load(quiz_dataset)
        slice = random.sample(quiz['questions'],5)    

    correct = 0 #Storing the correct answers
    for item in slice:
        not_answered = True
        while not_answered:
            print("\n" + item['Problem'])
            choice = input("YOU: ").lower()
            try:
                if (choice in TRUE_RESPONSE):
                    correct += item['Answer'] == "True"
                elif (choice in FALSE_RESPONSE):
                    correct += item['Answer'] == 'False'
                else:
                    raise Exception("Invalid input", choice) 
            except Exception:
                print("\nROBO: Please enter [True/Flase],[Yes/No] for answers.")
                print ("ROBO: I am crude so I will take it as an wrong answer. Just kidding :P.")
            else:
                not_answered = False
    print ("ROBO: You're finished, " + user_name + ". You got", correct, "out of 5 correct.")

def word_guessing():
    # https://www.geeksforgeeks.org/python-program-for-word-guessing-game/
    # https://medium.com/@4k45hr0ck5007/word-guessing-game-in-python-e30f7b176e32
    # library that we use in order to choose
    # on random words from a list of words

    with open('data/game_data.json', "r") as f:
        # Function will choose one random word from this list of words
        game_words = json.load(f)
        original_word = random.choice(game_words['words'])
        
    print(f"The word is of {len(original_word)} letters. ")

    wrong_list = []     # Record the letters guessed
    guessed_word = []   # Record the guessed word

    for i in range(len(original_word)):
        guessed_word.append("_")

    # any number of turns can be used here
    turns = 12
    
    while turns > 0:        
        # counts the number of times a user fails
        failed = 0
    
        # all characters from the input
        # word taking one at a time.

        valid_input = True
        print(*([i for i in guessed_word]))
        guess = input("\nGuess a character:")
        while valid_input:
            if not guess.isalpha():
                print('Guess only a letter')
            #check if guessed letter length is one or not
            elif(len(guess)>1):
                print('Guess only one letter...')
            #check that letter chosen by user is already guessed or not
            elif(guess in wrong_list):
                print('You have already guessed this letter')
            else:
                valid_input = True
                break
            print(*([i for i in guessed_word]))
            guess = input("\nRe-enter your guess:")

        turns -= 1
        #check if guess is matches with original_word
        if guess in original_word:
            for i in range(len(original_word)):
                if original_word[i] == guess:
                    guessed_word[i]=original_word[i] 
        else:
            print("You guessed WRONG letter.")
            print("You have", + turns, 'more guesses.')
            wrong_list.append(guess)
        guess_word = [i for i in guessed_word]
        guess_word = "".join(guess_word)

        if original_word ==guess_word :
            print("\nYou Win")
            print("The word is: ", original_word)
            return
     
    # if the character doesn’t match the word
    print("You Loose")
    print("The word is: ", original_word)

def small_adventure():
    print("adventure")

def game_selection(user_name):
    print("ROBO: which game do you want to play?")
    print("\t1) little quiz")
    print("\t2) word guessing")
    print("\t3) small adventure")

    selection = input("YOU: ")

    if not user_name:
        print("ROBO: Before we start the game, please tell me your name.")
        name = input ("YOU: ") #Storing the user's name
    else:
        name = user_name

    if selection == "little quiz":
        print ("ROBO: OK, " +  name + ", let's get started.")
        text_quiz(name)
    elif selection == "word guessing":
        print("ROBO: Good Luck! " + name)
        word_guessing()
    elif selection == "small adventure":
        print("ROBO: Let's go! " + name)
        small_adventure()

    return name
