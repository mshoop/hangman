# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:
# Hangman Game
# -----------------------------------

import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()

def is_word_guessed(secret_word, letters_guessed):
    """
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    """
    for letter in secret_word:
      if letter not in letters_guessed:
        return False
    return True

def get_guessed_word(secret_word, letters_guessed):
    """
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    """
    guessed_string = []
    for letter in secret_word:
      guessed = False
      for guess in letters_guessed:
        if letter == guess:
          guessed = True
          continue
      if guessed:
        guessed_string.append(f"{letter} ")
      else:
        guessed_string.append("_ ")
    return "".join(guessed_string)

def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    letters = string.ascii_lowercase
    available_letters = []
    for letter in letters:
      if letter in letters_guessed:
        continue
      else:
        available_letters.append(letter)    
    return "".join(available_letters)

def hangman(secret_word):
    """
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    """
    print("Welcome to the game Hangman!")
    print(f"I am thinking of a word that is {len(secret_word)} letters long.")
    score = len(secret_word)
    guess_number = 0
    total_guesses = 6
    total_warnings = 3
    letters_guessed = []
    while guess_number < total_guesses and is_word_guessed(secret_word, letters_guessed) is False:
      
      print(f"You have {total_guesses - guess_number} guesses left.")
      print(f"Available letters: {get_available_letters(letters_guessed)}")
      
      guess = input("Please guess a letter: ").lower()
      
      if not len(guess) == 1 and not guess.isalpha():
        total_warnings -= 1
        print("Only print 1 character from the alphabet")
        print("-------------"*2)
        continue

      if guess in letters_guessed:
        total_warnings -= 1
        if total_warnings <= 0:
          print(f"Oops! You've already guessed that letter. You now have no warnings left so you lose one guess: {get_guessed_word(secret_word, letters_guessed)}")
          guess_number += 1 
        else:
          print(f"Oops! You've already guessed that letter. You now have {total_warnings} warnings: {get_guessed_word(secret_word, letters_guessed)}")
        print("-------------"*2)
        continue
    
      letters_guessed.append(guess)
      
      if guess in secret_word:
        print(f"Good guess: {get_guessed_word(secret_word, letters_guessed)}")
      else:
        print(f"Oops! That letter is not in my word: {get_guessed_word(secret_word, letters_guessed)}")
        guess_number += 1
      print("-------------"*2)
    
    if is_word_guessed(secret_word, letters_guessed) is True:
      print("Congratulations, you won!")
      print(f"Your total score for this game is: {score}")
    
    if is_word_guessed(secret_word, letters_guessed) is False and guess_number == total_guesses:
      print(f"Sorry, you ran out of guesses. The word was '{secret_word}'.")
    

def match_with_gaps(my_word, other_word):
    """
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    """
    
    guessed_letters = []
    word_without_spaces = ""

    for character in my_word:

      if character != " ":
        word_without_spaces += character
            
      if character.isalpha():
        guessed_letters.append(character)

    if len(word_without_spaces.strip()) != len(other_word.strip()):
      return False 

    for index in range(len(word_without_spaces)):
      
      current_letter = word_without_spaces[index]
      other_letter = other_word[index]

      if current_letter.isalpha():

        same_letter = current_letter == other_letter

        if not same_letter:
          return False

      else:
        if current_letter == "_" and other_letter in guessed_letters:
          return False

    return True


def show_possible_matches(my_word):
    """
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    """
    matches = []
    for word in wordlist:
      if match_with_gaps(my_word, word):
        matches.append(word)
    if len(matches) > 0:
      for word in matches:
        print(word, end=" ")
    else:
      print("No matches found!")

def hangman_with_hints(secret_word):
    """
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    """
    print("Welcome to the game Hangman!")
    print(f"I am thinking of a word that is {len(secret_word)} letters long.")
    
    score = len(secret_word)
    guess_number = 0
    total_guesses = 6
    total_warnings = 3
    letters_guessed = []

    while guess_number < total_guesses and is_word_guessed(secret_word, letters_guessed) is False:
      print(f"You have {total_guesses - guess_number} guesses left.")
      print(f"Available letters: {get_available_letters(letters_guessed)}")
      guess = input("Please guess a letter: ").lower()
      
      if guess == "*":
        show_possible_matches(get_guessed_word(secret_word, letters_guessed))
        continue

      if not len(guess) == 1: #and not guess.isalpha():
        total_warnings -= 1
        print("Must only print 1 character from the alphabet")
        print("-------------"*2)
        continue
      
      if guess in letters_guessed:
        total_warnings -= 1
        if total_warnings <= 0:
          print(f"Oops! You've already guessed that letter. You now have no warnings left so you lose one guess: {get_guessed_word(secret_word, letters_guessed)}")
          guess_number += 1 
        else:
          print(f"Oops! You've already guessed that letter. You now have {total_warnings} warnings: {get_guessed_word(secret_word, letters_guessed)}")
        print("-------------"*2)
        continue
    
      letters_guessed.append(guess)
      
      if guess in secret_word:
        print(f"Good guess: {get_guessed_word(secret_word, letters_guessed)}")
      else:
        print(f"Oops! That letter is not in my word: {get_guessed_word(secret_word, letters_guessed)}")
        guess_number += 1
      print("-------------"*2)
    
    if is_word_guessed(secret_word, letters_guessed) is True:
      print("Congratulations, you won!")
      print(f"Your total score for this game is: {score}")
    
    if is_word_guessed(secret_word, letters_guessed) is False and guess_number == total_guesses:
      print(f"Sorry, you ran out of guesses. The word was '{secret_word}'.")


if __name__ == "__main__":
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
