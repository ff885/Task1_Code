import json
import random
import secrets
from pathlib import Path


math_symbols = {  # The operations that will appear in the question based on difficulty
    'Easy': ['+'],
    'Medium': ['+', '-'],
    'Hard': ['+', '-', '*', '//']
}

# QUESTION-RELATED FUNCTIONS
def num_of_question(difficulty):  # Num of questions for each difficulty level
    if difficulty == 'Hard': 

        value_1 = random.randint(1, 15)
        value_2 = random.randint(1, 15)  # 15 questions when 'Hard' mode is selected

    elif difficulty == 'Easy':
        value_1 = random.randint(1, 5)
        value_2 = random.randint(1, 5)  # 5 Questions when 'Easy' Mode is selected

    else:  # Num of questions for Medium Difficulty Level
        value_1 = random.randint(1, 10)
        value_2 = random.randint(1, 10)  # 10 questions when 'Medium' Mode is selected

    symbol = secrets.choice(math_symbols[difficulty])

    # Ensure division results in whole numbers
    if symbol == '/':
        value_1 = value_2 * random.randint(1, 10)  # Make sure value1 is a multiple of value_2

    if symbol == '+':
        correct_answer = value_1 + value_2
    elif symbol == '-':
        correct_answer = value_1 - value_2
    elif symbol == '*':
        correct_answer = value_1 * value_2
    elif symbol == '/':
        correct_answer = value_1 // value_2  # None of the answers will be decimals, just whole numbers

    question = f"{value_1} {symbol} {value_2} = ?"
    return question, correct_answer

def missing_num_question(difficulty):
    if difficulty == 'Hard':
        value_1 = random.randint(1, 15)
        value_2 = random.randint(1, 15)

    elif difficulty == 'Easy':
        value_1 = random.randint(1, 5)
        value_2 = random.randint(1, 5)

    else:  # Medium difficulty
        value_1 = random.randint(1, 15)
        value_2 = random.randint(1, 15)

    symbol = secrets.choice(math_symbols[difficulty])

    # Ensure division results in whole numbers
    if symbol == '/':
        value_1 = value_2 * random.randint(1, 10)  # Value_1 is a multiple of value_2

    # Determines which value the user has to calculate
    missing_num_position = random.choice([1, 2, 3])  

    if missing_num_position == 1:

        question = f"? {symbol} {value_2} = {value_1 + value_2}" if symbol == '+' else f"? {symbol} {value_2} = {value_1 - value_2}"
        correct_answer = value_1

    elif missing_num_position == 2:

        question = f"{value_1} {symbol} ? = {value_1 + value_2}" if symbol == '+' else f"{value_1} {symbol} ? = {value_1 - value_2}"
        correct_answer = value_2

    else:
        question = f"{value_1} {symbol} {value_2} = ?"
        correct_answer = value_1 + value_2 if symbol == '+' else value_1 - value_2

    return question, correct_answer


def generate_question(difficulty):  # Function to randomly choose between generating random arithmetic or missing number question

    difficulty = difficulty.capitalize()  # Ensure difficulty is in the correct format
    if random.choice([True, False]):

        return num_of_question(difficulty)
    
    else:
        return missing_num_question(difficulty)

def load_scoreboard():  # Function to load high scores from a JSON file
    file_path = Path('high_score_board.json')

    if not file_path.exists():
        score_default = {}
        return score_default
    
    else:
        with open(file_path, 'r') as file:
            return json.load(file)

def save_scoreboard(high_score):  # Saves the new score by overwriting the file's contents
    with open('high_score_board.json', 'w') as file:
        json.dump(high_score, file)

# Function that prompts user to select a difficulty 
def difficulty_choice():

### Prompts the user to select a difficulty level (Easy, Medium, Hard). 
### Returns: str: The selected difficulty level as a string ('Easy', 'Medium', 'Hard').
    
    while True:
        difficulty = input("Select a Difficulty Type: Easy, Medium or Hard\n").lower()
        if difficulty in ['easy', 'medium', 'hard']:
            break
        print("Try Again! Select a Difficulty Type: Easy, Medium or Hard")
    return difficulty.capitalize()  # Ensure it's returned in the correct format

# Displays the current high score for each difficulty
def high_score_board(high_score, user_name):
    print("HIGH SCORE BOARD for " + user_name )
    print(f"Hard: {high_score[user_name]['hard']}")
    print(f"Medium: {high_score[user_name]['medium']}")
    print(f"Easy: {high_score[user_name]['easy']}")

#MAIN GAME FUNCTIONS
def game_startup(): # Function to start the game (including user input and game rules)
    high_score = load_scoreboard()

    # Get or create the user
    user_name = input("What do you want to be called?\n(Retype your username if you are an existing player) \n")
    if user_name not in high_score:
        high_score[user_name] = {'easy': 0, 'medium': 0, 'hard': 0}
        save_scoreboard(high_score)
        print("Welcome to The Calculation Game, " + user_name + "!")
    else:
        print("Hello again," + user_name + "!")

    # Show current high scores
    high_score_board(high_score, user_name)

    # Skip game rules if user plays again
    if any(high_score[user_name][difficulty] > 0 for difficulty in ['easy', 'medium', 'hard']):

        print("\nCan you beat your old score or try a different level?")

    else:

        game_rules = '''\nHere's what you need to know :)
        \n1. Select a difficulty level for your game - Easy, Medium or Hard
        \n2. Do your best to solve all the calculations you are given!
        \n3. After each question, you'll find out if you were correct or not
        \n4. At the end of the game, your score (and any NEW high scores will be shown)
        \n5. Play again and see if you can do better! Good luck!!!!!\n '''

        print(game_rules)

    # Get a valid level input
    game_points = 0
    difficulty = difficulty_choice()

    # Setting the num of questions depending on difficulty
    if difficulty == 'Hard':
        question_total = 15
    elif difficulty == 'Easy':
        question_total = 5
    else:  # The alternative difficulty is Medium
        question_total = 10

    for _ in range(question_total):
        question, correct_answer = generate_question(difficulty)

        print(question)

        try:
            user_answer = float(input("Your answer: "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if user_answer == correct_answer:
            print("That's right! Next question.")
            game_points += 1
        else:
            print(f"Wrong answer :( The answer was meant to be {correct_answer}. Better luck next time!")

    print(f"Total score: {game_points}")

    if game_points > high_score[user_name][difficulty.lower()]:
        print(f"Congratulations {user_name}!\nYou've achieved a new high score for {difficulty}!")
        high_score[user_name][difficulty.lower()] = game_points
        save_scoreboard(high_score)

    # Ask if the user wants to play again
    play_again = input("This game has now ended.\n Press enter to play more or type bye to quit!!!").lower()
    if play_again != 'bye':
        game_startup()  # Recursively restart the game
    else:
        print("Thank you for playing! Goodbye!")

# Start the game
game_startup()
