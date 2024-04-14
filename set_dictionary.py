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

def get_word_length_frequencies(file_path: str) -> None:
    '''Print directly in pgfplot format coordinates of wwords length frequencies'''
    lengths = []
    with open(file_path, 'r') as file:
        for line in file:
            lengths.append(len(line.strip().split(':')[0]))
    for i in range(1, 18):
        counter = 0
        for el in lengths:
            if el == i:
                counter += 1
        print((i, counter))


trie = build_trie("dictionary.txt")
alphabet = set_alphabet("dictionary.txt")
# get_word_length_frequencies("dictionary.txt")