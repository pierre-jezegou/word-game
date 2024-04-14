''' The user act as a guesser - the programm gives scores for each letter'''
from additional_algorithms.string_words_manipulation import *
from tries import Trie
from wordle_keeper import *
from set_dictionary import *
import time

SECRET_LENGTH = 6
DICTIONARY_PATH = "dictionary.txt"
MAX_GUESSES = 10

def guesser_mode(trie: Trie,
                 word_length: int = SECRET_LENGTH,
                 dictionary_path: str = DICTIONARY_PATH,
                 max_attempts: int = MAX_GUESSES
                 ) -> None:

    secret = ''

    while len(secret) != word_length:
        secret = extract_informations(get_random_line(dictionary_path))
    result_array = [0 for _ in range(word_length)]
    attempts = 0
    print("Word length:", word_length)
    while not all(num == 2 for num in result_array) and attempts < max_attempts:
        user_input = user_word_input(len(secret))

        if not trie.search(user_input): # Test if the word is valid
            print("Your guess is not a valid word")
            continue

        result_array = check_guess(user_input, secret)
        attempts += 1

        if all(num == 2 for num in result_array):
            print(
                f"Well done, the word was %s.\nYou guessed it in %d attempts"
                % (secret, attempts))

        elif attempts == max_attempts:
            print(f"Try again... too many attempts.\nThe word was %s." % secret)

        else:
            print(''.join(map(str, result_array)))


def check_guess(guess: str, secret: str) -> list[int]:
    '''Check all letters for a guess and return the list of all status'''
    return [check_letter_status(guess[i], i, secret) for i in range(len(guess))]


def check_letter_status(letter: str, index: int, secret: str) -> int:
    '''Return status code for a letter presenc ein a word
        2: the letter and the index are good
        1: the letter is ok but not the index
        0: the letter nor the index are ok
    '''
    if letter == secret[index]:
        return 2

    return int(letter in secret)


def user_word_input(secret_length: int) -> None:
    user_input = input('Enter your guess: ')
    try:
        assert len(user_input)==secret_length
    except AssertionError:
        print(f"The word should be composed of %d characters" % secret_length)
    return user_input



def guesser_automatic_mode(word_length: int = SECRET_LENGTH,
                           dictionary_path: str = DICTIONARY_PATH,
                           max_attempts: int = MAX_GUESSES
                           ) -> None:

    # Initialisation section : trie, alphabet, secret
    secret = ''
    trie = build_trie(dictionary_path)
    alphabet = set_alphabet(dictionary_path)

    # Define secret (generated)
    while len(secret) != word_length:
        secret = extract_informations(get_random_line(dictionary_path))

    # Set puzzle
    result_array = [0 for _ in range(word_length)]
    attempts = 0
    guess = Guess(word_length, trie, alphabet)

    # Solve puzzle
    start_time = time.time()
    while not all(num == 2 for num in result_array) and attempts < max_attempts:
        guess.new_guess([int(score) for score in result_array])
        new_guess = guess.display_word()
        result_array = check_guess(new_guess, secret)

        attempts += 1
    end_time = time.time()

    return {
        'solved': all(num == 2 for num in result_array),
        'attempts': attempts,
        'max_attempts': max_attempts,
        'size': word_length,
        'cpu_time': end_time - start_time
    }
