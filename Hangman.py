import random
from GameView import HangmanView,BUTTON_ACTIVE,BUTTON_PRESSED
from time import sleep


LIVES = 9

'''
    Hangman model class defines the game behavior.
    It is initialized with a word in which each character must belong to a given dictionary.
'''

class Hangman:

    def __init__(self, word, alphabet):
        self.dictionary = {}
        self.word = word
        self.error_count = 0
        self.init_dictionary(alphabet)
        self.remaining_letters_count = len(self.dictionary.keys())
        self.previous_plays = []
        self.score = 0

    def init_dictionary(self, alphabet):
        if len(self.word) > 20:
            raise Exception("Input length must be less or equal to 20 characters.")
        for i in range(0, len(self.word)):
            if self.word[i] == ' ':
                continue
            elif self.word[i] not in alphabet:
                raise Exception(self.word[i], " not in alphabet.")
            elif self.word[i] not in self.dictionary.keys():
                self.dictionary[self.word[i]] = [i]
            else:
                self.dictionary[self.word[i]].append(i)

    def play(self, letter):
        if self.has_won() or self.has_lost():
            return "Oops! The game is over!"
        elif letter in self.previous_plays:
            return "You have already selected " + letter + "."
        elif letter in self.dictionary.keys():
            self.previous_plays.append(letter)
            self.remaining_letters_count -= 1
            return self.dictionary.get(letter)
        else:
            self.previous_plays.append(letter)
            self.error_count += 1
            return "Oops! " + letter + " is not part of the solution."

    # Losing condition.
    def has_lost(self):
        return self.error_count == LIVES

    # Winning condition.
    def has_won(self):
        return self.remaining_letters_count == 0

if __name__ == "__main__":
    # Initialize the views and word generator.
    game_view = HangmanView(1000, 600)

    # English alphabet.
    alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
                "V", "W", "X", "Y", "Z"]

    words = ["PYTHON", "JAVASCRIPT", "RUBY", "JAVA", "HTML", "SWIFT"]
    
    # Game loop...
    while True:
        # Initialize Hangman Model with a random word and alphabet.
        random_word = random.choice(words)
        hangman = Hangman(random_word, alphabet)

        game_view.update_image(0)

        # Draw buttons to their initial state.
        for i in range(0, len(alphabet)):
            game_view.draw_button(i, BUTTON_ACTIVE, alphabet[i])

        # Draw initial word blanks.
        for i in range(0, len(random_word)):
            if random_word[i] == ' ':
                game_view.draw_character(i, ' ')
            else:
                game_view.draw_character(i, '_')

        # While on the current game.
        while not hangman.has_won() and not hangman.has_lost():
            player_input = game_view.button_pressed_scanner()
            if player_input is None:  # Nothing happened.
                continue
            elif player_input == -1:  # Reload Button Pressed.
                game_view.draw_feedback("Let's start from scratch.")
                sleep(2)
                break
            else:  # A character button was pressed.
                letter = alphabet[player_input]
                response = hangman.play(letter)
                game_view.draw_button(player_input, BUTTON_PRESSED, letter)
                if type(response) is not str:
                    for j in range(0, len(response)):
                        game_view.draw_character(response[j], letter)
                    response = letter + " is part of the solution."
                game_view.update_image(hangman.error_count)
                game_view.draw_feedback(response)
                
        game_view.draw_feedback("Game Over!")
        sleep(3)
        if hangman.has_lost():
            game_view.draw_feedback("You lose. :|")
        elif hangman.has_won():
            game_view.draw_feedback("You win! :D")


        sleep(5)
        game_view.clear_word()
        game_view.draw_feedback("")



