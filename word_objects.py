from random import choice, shuffle

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

    def is_new_letter(self, new_letter: str) -> bool:
        return not new_letter in self.past_letters

    def block_letter(self) -> None:
        self.blocked_letter = True

    def add_letter_guess(self, letter: str) -> None:
        self.past_letters.add(letter)
        self.current_letter = letter

    def is_past_letter(self, letter: str) -> bool:
        return letter in self.past_letters


class Guess():
    def __init__(self,
                 length: int,
                 alphabet: list[str] = ALPHABET
                 ) -> None:
        '''Init guess object'''

        self.letters: list[WordLetter] = [WordLetter(i) for i in range(length)]
        self.length: int = len(self.letters)
        self.alphabet: list[str] = alphabet
        self.incorrect_position_letters : set = set()
        self.bad_letters: set = set()
        self.remaining_letters: int = self.length

    def display_word(self) -> None:
        '''Print word - result in str'''
        word: str = ""
        for letter in self.letters:
            if letter.current_letter is None:
                word += "_"
            else:
                word += letter.current_letter
        return word

    def actualize_letter(self,
                         letter: WordLetter
                         ) -> None:
        '''Actualize letter object with the new guess'''
        possible_letters = list(self.incorrect_position_letters)
        shuffle(possible_letters)
        # print("Possible letters:", possible_letters)
        try:
            for l in possible_letters:
                print("Possible letter:", l)
                if l not in letter.past_letters:
                    return letter.add_letter_guess(l)
        except TypeError:
            pass

        l = extract_random_letter()
        while l in self.bad_letters or letter.is_past_letter(l):
            l = extract_random_letter()

        letter.add_letter_guess(l)

    def actualize_letters_informations(self, scores: list[int]) -> None:
        '''Set letter informations depending on score array'''
        for i in range(self.length):
            self.letters[i].score = scores[i]
            if scores[i] == 2:
                self.letters[i].block_letter()
                self.incorrect_position_letters.discard(self.letters[i].current_letter)
            if scores[i] == 1:
                self.incorrect_position_letters.add(self.letters[i].current_letter)
            else:
                self.bad_letters.add(self.letters[i].current_letter)

    def new_guess(self, result_scores: list[int]) -> str:
        '''Main function to create a new guess'''
        self.actualize_letters_informations(result_scores)

        for letter in self.letters:
            if not letter.blocked_letter: # To limit function scope
                self.actualize_letter(letter)

        return self.display_word()



def extract_random_letter(alphabet: list[str] = ALPHABET
                          ) -> str:
    '''Extract random element from given alphabet'''
    return choice(alphabet)


def main():
    length_input = int(input("Word length: "))
    guess = Guess(length_input)
    results = [0 for i in range(length_input)]
    while results != [2 for i in range(length_input)]:
        print("-"*10)
        print("Blocked letters: ", guess.bad_letters)
        print("Bad position letters: ", guess.incorrect_position_letters)
        print("Results: ", results)
        print(guess.new_guess(results))
        user_input = input("Compute score: ")
        results = [int(user_input[i]) for i in range(len(user_input))]


if  __name__=="__main__":
    main()