from string_words_manipulation import *
from tries import Trie

SECRET_LENGTH = 4
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
    print(secret)
    result_array = [0 for _ in range(word_length)]
    attempts = 0

    while not all(num == 2 for num in result_array) and attempts <= max_attempts:
        user_input = input('Enter your guess: ')
        try:
            assert len(user_input)==len(secret)
        except AssertionError:
            print(f"The word should be composed of %d characters" % word_length)
            continue

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
            print("Try again... too many attempts")

        else:
            print(''.join(map(str, result_array)))


def check_guess(guess: str, secret: str) -> list[str]:
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

