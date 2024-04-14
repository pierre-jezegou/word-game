''' The user act as a keeper
    The programm gives word guesses and the user provide scores for each letter
'''
from random import choice, randint
import time
from tries import Trie

ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

class WordLetter():
    '''[Keeper Mode] Define class to model a letter in a word in Wordle Game'''
    def __init__(self, index: int) -> None:
        '''Init'''
        self.index: int = index
        self.past_letters: set = set()
        self.score: int = 0
        self.blocked_letter: bool = False
        self.current_letter: str = None

    def update_score(self, new_score: int) -> None:
        '''Update score'''
        self.score = new_score

    def block_letter(self) -> None:
        '''Set `blocked_letter to True to limit scope of word search'''
        self.blocked_letter = True

    def add_letter_guess(self, letter: str) -> None:
        '''Set current letter to the given letter'''
        self.current_letter = letter

    def is_past_letter(self, letter: str) -> bool:
        '''Compare th enew letter with the past letters'''
        return letter in self.past_letters

    def add_past_letter(self, letter: str) -> None:
        '''Add the letter to already used letters (to limit future tests)'''
        self.past_letters.add(letter)


class Guess():
    '''Implement guess class for keeper mode'''
    def __init__(self,
                 length: int,
                 dictionary_trie: Trie,
                 alphabet: list[str] = ALPHABET
                 ) -> None:
        '''Init guess object'''

        self.letters: list[WordLetter] = [WordLetter(i) for i in range(length)]
        self.length: int = len(self.letters)
        self.alphabet: list[str] | set[str] = alphabet
        self.incorrect_position_letters : set = set()
        self.bad_letters: set = set()
        self.remaining_letters: int = self.length
        self.dictionary_trie: Trie = dictionary_trie

    def display_word(self) -> str:
        '''Print word - result in str'''
        word: str = ""
        for letter in self.letters:
            if letter.current_letter is None:
                word += "_"
            else:
                word += letter.current_letter
        return word

    def is_valid_word(self, word: str) -> bool:
        '''Return true if the given word in registered in the dict'''
        return self.dictionary_trie.search(word)

    def actualize_letter(self,
                         letter: WordLetter
                         ) -> None:
        '''Actualize letter object with the new guess'''
        # possible_letters = list()
        # shuffle(possible_letters)
        try:
            for l in self.incorrect_position_letters:
                if l not in letter.past_letters and randint(0,1):
                    return letter.add_letter_guess(l)
        except TypeError:
            pass

        l = self.extract_random_letter()
        counter = 1
        while (l in self.bad_letters or letter.is_past_letter(l)) or counter <= len(ALPHABET):
            l = self.extract_random_letter()
            counter += 1

        return letter.add_letter_guess(l)

    def actualize_letters_informations(self, scores: list[int]) -> None:
        '''Set letter informations depending on score array'''
        for i in range(self.length):
            self.letters[i].score = scores[i]
            if scores[i] == 2:
                self.letters[i].block_letter()
                self.incorrect_position_letters.discard(self.letters[i].current_letter)
            elif scores[i] == 1:
                self.incorrect_position_letters.add(self.letters[i].current_letter)
            else:
                self.bad_letters.add(self.letters[i].current_letter)


    def generate_new_letters(self) -> None:
        '''Geerate new letters attempts for non found letters'''
        for letter in self.letters:
            if not letter.blocked_letter: # To limit function scope
                self.actualize_letter(letter)


    def new_guess(self, result_scores: list[int]) -> str:
        '''Main function to create a new guess'''
        self.actualize_letters_informations(result_scores)
        self.generate_new_letters()

        while not self.is_valid_word(self.display_word()):
            self.generate_new_letters()

        for letter in self.letters:
            letter.add_past_letter(letter.current_letter)

        return self.display_word()



    def extract_random_letter(self) -> str:
        '''Extract random element from given alphabet'''
        return choice(list(self.alphabet))


def keeper_interactive_mode(dictionary_trie: Trie,
                            alphabet: set[str] | list[str] = ALPHABET):
    '''Interactive mode'''
    length_input = int(input("Word length: "))
    guess = Guess(length_input, dictionary_trie, alphabet)
    results = [0 for i in range(length_input)]
    while results != [2 for i in range(length_input)]:
        print("-"*10)
        start_time = time.time()
        print(guess.new_guess(results))
        end_time = time.time()
        print("\tGuess time:", end_time - start_time)
        print("\tBlocked letters: ", guess.bad_letters)
        print("\tBad position letters: ", guess.incorrect_position_letters)
        print("\tResults: ", results)
        user_input = input("Compute score: ")
        results = [int(user_input[i]) for i in range(len(user_input))]