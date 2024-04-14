from wordle_guesser import *
from wordle_keeper import *
from set_dictionary import *
import json
# from typing import Tuple


SECRET_LENGTH = 4
DICTIONARY_PATH = "words_alpha.txt"
MAX_GUESSES = 10

alphabet = set_alphabet(DICTIONARY_PATH)
dictionary_trie = build_trie(DICTIONARY_PATH)

AUTOMATIC_MODE = True
AUTOMATIC_MODE_GENERATOR = True
GUESSER = False
KEEPER = True


if __name__=="__main__":
    # keeper_interactive_mode(dictionary_trie, alphabet)
    # guesser_mode(dictionary_trie, 6, DICTIONARY_PATH, 2)
    # print(guesser_automatic_mode())
    results = []
    if AUTOMATIC_MODE and AUTOMATIC_MODE_GENERATOR:
        for i in range(3, 6):
            for _ in range(200):
                result = guesser_automatic_mode(word_length=i)
                print(result)
                results.append(result)

    elif AUTOMATIC_MODE:
        guesser_automatic_mode()
    else :
        if GUESSER:
            guesser_mode(dictionary_trie)
        if KEEPER:
            keeper_interactive_mode(dictionary_trie, alphabet)
    
    
    with open('exports/automatic_wordle.json', 'w') as f:
        json.dump(results, f)