import time
import json
import random
import systems.adventure.mainGame as ag

def text_quiz():
    """
        Perform a round of quiz game.

        Returns: return the player's score after the quiz.
    """

    TRUE_RESPONSE = ["t", "true", "yes", "y"]
    FALSE_RESPONSE = ["f", "false","no", "n"]

    print ("ROBO: Remember, the following answers are only True or False.")
    print ("Evaluating your intelligence level...")
    time.sleep(0.3)
    print ("Searching database for quiz problems...")
    time.sleep(0.5)
    
    # Load questions from the database
    with open('data/game_data.json', "r") as quiz_dataset:
        quiz = json.load(quiz_dataset)
        slice = random.sample(quiz['questions'],5)    # Randomly select 5 questions from the database

    correct = 0 #Storing the correct answers
    for item in slice:
        not_answered = True
        while not_answered:
            print("\n" + item['Problem'])
            choice = input("YOU: ").lower()
            # A mechanism to ban invalid answers
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
    return correct

def word_guessing():
    """
        Perform a round of word gueesing game.
    """
    with open('data/game_data.json', "r") as f:
        game_words = json.load(f)
        # Function will choose one random word from this list of words
        original_word = random.choice(game_words['words'])
        
    print(f"The word is of {len(original_word)} letters. ")

    wrong_list = []     # Record the wrong letters guessed
    guessed_list = []   # Record the letters guessed
    guessed_word = []   # Record the guessed part of original_word

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
        print()
        print(*([i for i in guessed_word]))
        guess = input("\nGuess a character:")
        while valid_input:
            if not guess.isalpha():
                print('Guess only a letter...')
            #check if guessed letter length is one or not
            elif(len(guess)>1):
                print('Guess only one letter...')
            #check that letter chosen by user is already guessed or not
            elif(guess in wrong_list or guess in guessed_list):
                print('You have already guessed this letter')
            else:
                valid_input = True
                break
            print()
            print(*([i for i in guessed_word]))
            guess = input("\nRe-enter your guess:")

        turns -= 1
        #check if guess is matches with original_word
        if guess in original_word:
            guessed_list.append(guess)
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
     
    # if the user used up his/her turn
    print("You Loose")
    print("The word is: ", original_word)

def pipeline(user_name, robot_name):
    """
        General procedure for this sub system.
    """
    print(robot_name + ": which game do you want to play?")
    print("\t1) little quiz")
    print("\t2) word guessing")
    print("\t3) small adventure")

    selection = input("> ")

    if not user_name:
        print(robot_name + ": Before we start the game, please tell me your name.")
        name = input ("> ") #Storing the user's name
    else:
        name = user_name

    if selection == "little quiz" or selection == '1':
        print (robot_name + ": OK, " +  name + ", let's get started.")
        res = text_quiz()
        print (robot_name + ": You're finished, " + user_name + ". You got", res, "out of 5 correct.")

    elif selection == "word guessing" or selection == '2':
        print(robot_name + ": Good Luck! " + name)
        word_guessing()

    elif selection == "small adventure" or selection == '3':
        print(robot_name + ": Let's go! " + name)
        ag.pipeline()

    return name

# To test the sub system, invoke pipeline here
pipeline("Chenkai", "Jarvis")
