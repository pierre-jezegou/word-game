from wordle_guesser import *
from wordle_keeper import *
from additional_algorithms.set_dictionary import *
# from typing import Tuple


SECRET_LENGTH = 4
DICTIONARY_PATH = "words_alpha.txt"
MAX_GUESSES = 10

alphabet = set_alphabet(DICTIONARY_PATH)
dictionary_trie = build_trie(DICTIONARY_PATH)



if __name__=="__main__":
    print(dictionary_trie.search("bit"))
    keeper_interactive_mode(dictionary_trie, alphabet)