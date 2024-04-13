'''Interactions with dictionary'''
from tries import Trie

def build_trie(file_path: str) -> Trie:
    '''Get random line from a goven file'''
    dictionary_trie = Trie()

    with open(file_path, 'r') as file:
        for line in file:
            dictionary_trie.insert_word(line.strip().split(':')[0])

    return dictionary_trie

def set_alphabet(file_path: str) -> set[str]:
    '''Extract eveny character from a given dictionary to build an alphabet'''
    dictionary_alphabet = set()

    with open(file_path, 'r') as file:
        for line in file:
            word = line.strip().split(':')[0]
            for _, letter in enumerate(word):
                dictionary_alphabet.add(letter)

    return dictionary_alphabet

trie = build_trie("dictionary.txt")
alphabet = set_alphabet("dictionary.txt")
