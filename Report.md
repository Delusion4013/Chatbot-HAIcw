# Chenkai’s Chatbot Report

## 1. Introduction

I wanted to build a general purpose chatbot which is easily extendable and modifiable. Therefore I implemented a `Chatbot` class with fundemental functions (like intent management and data loading) and  different sub-systems to load, where each sub-system correspond to one intent. 

In this way, we could easily modify the applicable scenario by adjusting the sub-systems loaded.

### 1.1 Reasoning - Why these features?

The complete list of features implemented could be found in [section 3](#3. Proposed system).

The reasons for choosing **intent management** is simple: all multi-functional chatbots need an intent routing mechanism to decide how to perform.To be specific, different types of tasks requires different pipeline for handling input and generating output.

The reasons for choosing **identity management** is then an attempt to explore on NLU filed. Only with the mechinism for some sort of entity recognition could this task be accomplished. Meanwhile, identity management requires the chatbot being able to store and retrieve data/information. Implementing this feature could then enable the chatbot to manage data input during operation. 

## 2. Background

During my conception of this coursework project, I have seen numerous instances of Chatbots on the Interent and examined their implementations.

When receiving the coursework description, I started reading this [book](https://github.com/PacktPublishing/Hands-On-Chatbot-Development-with-Alexa-Skills-and-Amazon-Lex). This book gives me some background knowledge about the basic components of chatbots. In Chapter *Understanding Chatbots*, I learned about the basic components of chatbots, like intents, slots, utterances. It also provides a good example about how to design a conversation flow. 

At the early stage, this [chatbot-1](https://github.com/parulnith/Building-a-Simple-Chatbot-in-Python-using-NLTK) gives me some ideas about how to perform basic greeting functions and let me started on this coursework. Its process on information retrieval also gives me some inspirations. 

When I was trying to build intent management system for this chatbot, I came across this well-structured [chatbot-2](https://github.com/mtaruno/eve-bot). The relevant [blog post](https://towardsdatascience.com/complete-guide-to-building-a-chatbot-with-spacy-and-deep-learning-d18811465876) gives me inspiration about how to do the intent classification using machine learning models and how to structure the chatbot with different intents. However, as I want my chatbot to be flexible on its functions with different sub-systems equipped, I did not implement such intent management system which based on pre-definition on chatbot’s intents.

There are also a lot of other wonderful blog posts, github repositories and relevant bookds that inspired me during my journey on building this bot. Due to limitation on spaces, I will add them in [appendix](#Appendix) and attach a brief note about what role it played.

## 3. Proposed system

In this coursework, I have implement the chatbot with features:

1. **Intent management**
2. **Identity management**
3. **Information retrieval**
4. **Text based games**
4. **Small talk system**

The file architecture is as follows:

```
Chatbot-HAIcw
├─ .gitignore
├─ Chatbot.py (main Chatbot class)
├─ README.md
├─ Report.md 
├─ data		(storing the data to be used for different systems)
│  ├─ game_data.json
│  ├─ qa.csv
│  ├─ qa.json
│  └─ user_profile.json
├─ main.py	(the script to start the chatbot)
├─ scripts  (some helper/explorative scripts that are used in chatbot)
│  ├─ explorative.ipynb
│  └─ script.ipynb (script to convent qa.csv into qa.json)
├─ systems 	(sub-systems that the Chatbot equips)
│  ├─ game.py
│  ├─ identity_managment.py
│  ├─ information_retrieval.py
│  └─ small_talk.py
└─ test	    (Store the testing instructions and prompt result)
   ├─ sampleOutput-Game.txt
   ├─ sampleOutput-IM.txt
   ├─ sampleOutput-IR.txt
   ├─ sampleOutput-general.txt
   └─ testScript.md

```


Bleow is an overview procedure of this chatbot (i.e. the `general_pipeline() ` in `Chatbot` class).

<center><img src="/Users/chenkaihu/Downloads/general.png" alt="general" style="zoom:80%;" /></center>



### 3.1 Intent management

- Functionality

    Take user’s input and deduce user’s possible intent, then **invoke the relevant sub-systems.**

- Originality

    Unlike many other chatbots, this chatbots uses more text-based and template matching for intent routing. This is to cope with aim of implementing the chatbot with the flexibility for modifiable intents.

- Implementation

    In this chatbot, intent management are built in `Chatbot` class using the method `intent_match()`. A key-word / pattern matching mechanism is used to invoke different sub-systems.

    The overall procedure is as following snippet:

    ```python
    def intent_match(self, user_response):
            if (user_response == 'menu' or user_response == 'help'):
                self.show_menu()
            elif (user_response == 'qa' or user_response == 'IR'):
                IR.pipeline(self.robot_name)
            elif (user_response == 'games'):
                self.user_name = game.pipeline(self.user_name, self.robot_name)
                self.name_get = True
			...
            return
    ```
    
    

### 3.2 Identity management

- Functionality

    Asks for, store and retrieve user’s name for other usage in proper context.

- Originality

    - Add storage & retrieval process for user’s identity information when chatbot initialize and terminates. This could preserve the user’s information processed during usage.
    - Used chunking techniques[^1] to detect name entities.

- Implementation

    The implementation could be found in `systems/identity_management.py`.

    When the user shows intent of asking stored name, this system would be invoked.

    [^1]: This refers to the `nltk.ne_chunk module`.
    
    

### 3.3 Information retrieval

- Functionality

    Given a query, prompt the most relevant information / question answer pairs in the database.

- Originality

    - Though the database used is a qa-database, I add small tricks on deciding whether the user’s input is a question or not, then generate resposne correspondingly. 
    - Meanwhile, I have implemented preprocess pipeline for input data (method `preprocess(query)`) and general methods for creating model and perfrom search. Therefore it could adapt to new corpuse with little modifications.

- Implementation

    The detailed implementation could be found in `systems/informatino_retrieval.py`.

    In general, the model retrievals relevant information based on cosine similarity between user’s query and database entries. It will continously asks the user to input query unless an ending command (`quit`) is received.

    In `search(query)` method, a `TfidfVectorize`[^2]  was used to build the language model, the cosine similarity are calculated and the most relevant information’s index is returned.

    [^2]: This model was from `sklearn` library.

    

### 3.4 Text based games

Two games are implemented and could be selected from the menu when user shows the intent of playing games.

#### 3.4.1 Small Quiz

- Functionality

    The quiz game would select several questions from the database and asks you to input your answer. 

- Originality

    Unlike the [inspiration bolg](https://www.derekshidler.com/how-to-create-a-text-based-adventure-and-quiz-game-in-python/), I modified my version of quiz game using database to store the questions.

- Implementation

    The quiz was implemented in the method `system/game.text_quiz()`. The game procedure could be generalized as:

    1. Obtaining questions from the database
    2. Iteratively ask user to prompt answer for each question (Handles invalid input during the process)
    3. Return the result

#### 3.4.2 Word Guessing

- Functionality

    The word guessing game which randomly selects a word in the database and ask the user to guess the word with predifined procedure. 

- Originality

    The game took inspiration form these two blogs: [blog1](https://www.geeksforgeeks.org/python-program-for-word-guessing-game/), [blog2](https://medium.com/@4k45hr0ck5007/word-guessing-game-in-python-e30f7b176e32). I combined the game procedure from those two blogs and beautified the prompt messages.

- Implementation

    The word guessing game was implemented in the method `system/game.word_guessing()`.
    
    The game procedure are as follows:
    
    1. Randomly select a word from the database.
    2. Iteratively ask the user to type in a character (Handles invalid input) and check it.
    3. Terminate the guessing process if all turns are used.

### 3.5 Small talk

- Functionality

    When detected pre-defined inputs, enter this system and generates response with the database.

- Originality

    Instead of using dynamic NLG techniques (like network approaches),  template-based response are used to avoid uncertainty or even biased messages.

- Implementation

    The small talk system would respond to pre-defined set of inputs and generates corresponding outputs. It’s implemented as a rule-based system.

## 4. Evaluation

The project was tested with suggested test script and user testing. The test guidance are included in file `test/testScript.md`, where basic settings, testing commands and procedures are listed.

- For the **suggested test script**, tests are designed to see how chatbot react to expected valid inputs and invalid inputs.
- For **user testing**, the general procedure is evaluated to see if the chatbot is easy to use together with sub-systems.

### 4.1 Testing of Intent classification

Mostly user’s testing. Users are required to **use different sub-systems in different orders** to see if all systems co-operates well. For example, IM system would store the user name information for Game system.

### 4.2 Testing of Identity management

Tests are done by both suggested script and user’s random inputs.

- [x] Pre-loaded result
- [x] Valid inputs
- [x] Invalid inputs
- [x] Quit the system

### 4.3 Testing of Information retrieval system

Tests are done by both suggested script and user’s random inputs.

- [x] Entering & quiting IR system
- [x] Query for questions
- [x] Query for information
- [x] Invalid input

### 4.4 Testing of Game system

Tests are done by both suggested script and user’s random inputs.

- [x] Game selection
- [x] Quiz game
    - [x] valid inputs
    - [x] Invalid inputs
- [x] Guessing game
    - [x] valid inputs
    - [x] Invalid inputs
- [x] Adventures
- [x] Cooperation with IM system



## 5. Discussion

### 5.1 Results of Evaluation

The results of evaluation could be found in relevant script files (in the `test/` folder) storing the conversation between user and chatbot. 

In general, all functions operates as expected and is consistent with the performance when I (as the developer) did the testing. However, small bugs occured and was fixed later on. Also some suggestions are acquired from users (included in [section 6.2](#6.2 Possible extensions)) and the relevant templates are enriched..

### 5.2 Possible bias

Below are some recorded conversations fragments between user and the bot that attracts my attention.

1. Chinese names compared with English names

    ```
    test/sampleOutput-IM
    
    Standard inputs - 4 Simple invalid inputs (Name cannot be tagged)
    ...
    Jarvis: You didn't tell me your name! Please tell me and I will keep it down.
    > Chenkai is my name
    Jarvis: No name detected in former input. Please try again...
    Jarvis: Type [quit] to terminate this process.
    > Chenkai HU is my name
    Jarvis: Got you! Chenkai Hu
    ...
    
    User inputs - 1 Unexpected inputs when asking name
    ...
    YOU: what is my name?
    Jarvis: You didn't tell me your name! Please tell me and I will keep it down.
    > Eric is my english name
    Jarvis: I will keep it in my database Eric
    ...
    ```

    In the conversation above, `Chenkai` (my chinese name) could not be tagged as a name while `Eric` (A typical English name) can. It is also against the Chinese name conventsion where Chinese tend to keep all their family name in upper case (`HU` is automatically transferred to `Hu` in this case). 

    With careful analysis, I suppose this is caused by the chunking mechanism built in `nltk`. 

2. Improper/Incomplete information for IR system

    ```
    User inputs - 2 Query for information (No related info found)
    ...
    > Tell me about Eason Chen 
    Jarvis: Searching.....
    I am sorry! Nothing relevant found in my database.
    ...
    
    User inputs - 1 Query for question
    ...
    > who is president obama
    Jarvis: Searching.....
    Founded the most relevant question in database.
    Q: when barack obama was born?
    A: Barack Hussein Obama II (; born August 4, 1961) is the 44th and current President of the United States , the first African American to hold the office.
    ...
    ```

    For example, in the above conversation, information about my favorite singer (Eason) are not included while President obama could be found. 

    This rings me the bell that there may be incomplete messages included in the QA database which lead to deadly decisions (e.g. medical treatments). There may also be improper information contained in the original database (e.g. racist answers). 

### 5.3 Reflections

Overall, I have implemented the chatbot in a way that is not dependent on third parties’ input data or any hardly explainable AI techniques to avoid possible discriminations or bias. Special care need to be taken when choosing the database for information retrieval.

As for the potential impact, I think my chatbot will do the pre-defined tasks well but lose some flexibility when facing new inputs.

## 6. Conclusion

Generally speaking, a chatbot architecture supporting flexible sub systems are implemented. Five sub-systems are implemented, either intergrated in the Chatbot class (i.e. intent management), or seperated for usage. 

### 6.1 Project management

The project used `git` for version controls.

The tasks are not distributed evenly among the 4 weeks, some development tasks and report tasks are underestimated in the aspect of time needed.

### 6.2 Possible extensions

- For intent management
    - A machine learning based model (or `IntentClassifier`) could be implemented to enhance bot’s capability in more generalized form of intent detecting.
- For identity management
    - More entity recognition could be added to enhance the information the bot could extract and store. For example, extract entities like locations or phone number. This could provide more information when bot interacting with users (Just like Siri :P). 
    - Dig into relationship between different person entities. For example, when the user says ‘Lucy is my sister’, the bot could extract the relationship and sotre them properly (Just like Contacts). 
- For information retrieval
    - A more generalized corpus could be used. The current QA corpus have some limitations.
    - A more structured retrieval system could be designed. For example, when the user’s input shows no inclinations, search the general database, if the user shows an interest in, say, books, then search the book database with more detail.
    - Index based system could be built when arranging large scale corpus. It’s like how searching engines are now arranging their corpus. `Elasticsearch` may be a promising framework to use here. 
- For small talk
    - Use dyanmic NLG techniques to add some uncertainty and entertainment when communicating.

## Appendix

1. [NLTK book](https://www.nltk.org/book) - The book gives me an overview of NLTK packages and many common example tasks using this library.
    - Chapter 2 : Accessing Text Corpora and Lexical Resources - A useful introduction for existing corpora in nltk.
    - Chapter 6: Learnign to classify Text - Startup guide on classification using ML techniques
    - Chapter 7: Extracting Information from Text - A useful introduction for explaining tagging & entity recognition.
2. [Blog post from Pratheesh Shivaprasad](https://towardsdatascience.com/how-to-build-a-basic-chatbot-from-scratch-f63a2ccf5262) - This blog gives me some inspirations on how to sructure intents using templates, as well as the idea of how to build a transactional system for ordering.
3. [Blog post from Sharif](https://www.aionlinecourse.com/blog/how-to-build-and-deploy-a-restaurant-chatbot-with-rasa-and-python) - Though using Rasa, the archiecture is really inspiring.
4. [Repo from Apress](https://github.com/Apress/building-an-enterprise-chatbot) - Not viewed in much detail, but proivdes a valid solution for NLG problem.
