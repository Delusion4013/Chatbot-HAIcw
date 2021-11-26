

# How to run this project?

## Pre-requisites

- `python`
- `nltk`
- `sklearn`

## Run

Navigate to the code folder and execute `main.py`.

```python
> $ cd Chatbot-HAIcw
> $ python main.py
```



# General commands

This chatbot is case-insensitive unless you are prompting your name.

- `menu` / `help`: a menu would popup and shows the relevant features implemented.
- Try saying `thank you` to the bot.
- `bye` to terminate the chatbot.

# Sub-systems

## 1. Identity Management

> ==To test this sub-system, ask for your name like: `what is my name?` ` who am i?`==

If the name are not stored, this system would require your input as the name. Just follow the instructions prompted.

>The system will terminate automatically when a name is collected. If keep getting errors, type `quit` to terminate this process.

## 2. Information Retrieval

> ==To test this sub-system, type qa in the command line when not in other systems==

You could structure your query like:

- `how are antibodies used?`
- ``antibodies binding mechanism`
- `tell me about Singer Bob Seger`

> To quit the system, type `close`



## 3. Text based games

>  ==To test this sub-system, type ‘game’ when not in other systems==

Type the prompt game name or its index number for different game.

### Quiz

- Follow the instructions, give answers (could be `True/False`, `T/F`) to different questions.
- You could try other inputs for checking the error handling.

### Word guessing

- Follow the instructions, enter characters you guess.
- You could try other inputs (like multiple characters, non-character, guessed letters)

> The system will terminate automatically when a round of game is finished.

## 4. Small talk

> ==To test this sub-system, just type in the question like below.==

Small talk like:

- greetings, 
- ‘How’s weather?’, ‘Tell me about the weather’
- ‘How are you?’, ‘How’s everything going?’

The bot would respond to the listed questions.

> The system will terminate automatically when a response was generated.