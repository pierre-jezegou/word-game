'''Implement guesser part of the wordle game'''
from random import choice, randint
from tries import Trie
import time

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


# # dictionary = ['ACE', 'ACT', 'ADD', 'ADS', 'AFT', 'AGE', 'AGO', 'AID', 'AIM', 'AIR', 'ALE', 'ALL', 'AND', 'ANY', 'APE', 'APT', 'ARC', 'ARE', 'ARK', 'ARM', 'ART', 'ASH', 'ASK', 'ASP', 'ATE', 'AUK', 'AVE', 'AWE', 'AWL', 'AXE', 'AYE', 'BAD', 'BAG', 'BAH', 'BAN', 'BAR', 'BAT', 'BAY', 'BED', 'BEE', 'BEG', 'BET', 'BEY', 'BIB', 'BIG', 'BIN', 'BIT', 'BOA', 'BOB', 'BOD', 'BOG', 'BOO', 'BOP', 'BOT', 'BOX', 'BOY', 'BUB', 'BUD', 'BUG', 'BUM', 'BUN', 'BUS', 'BUT', 'BUY', 'BYE', 'CAB', 'CAD', 'CAM', 'CAN', 'CAP', 'CAR', 'CAT', 'CAW', 'CAY', 'COD', 'COG', 'CON', 'COO', 'COP', 'COT', 'COW', 'COY', 'CRY', 'CUB', 'CUE', 'CUP', 'CUR', 'CUT', 'DAB', 'DAD', 'DAM', 'DAN', 'DAY', 'DEN', 'DEW', 'DID', 'DIE', 'DIG', 'DIM', 'DIN', 'DIP', 'DOE', 'DOG', 'DON', 'DOT', 'DRY', 'DUB', 'DUD', 'DUE', 'DUG', 'DUO', 'DYE', 'EAR', 'EAT', 'EEL', 'EGO', 'ELF', 'ELK', 'ELM', 'EMU', 'END', 'ERA', 'ERR', 'ESP', 'ETA', 'EVE', 'EWE', 'EYE', 'FAD', 'FAG', 'FAN', 'FAR', 'FAT', 'FAY', 'FED', 'FEE', 'FEW', 'FIB', 'FIG', 'FIN', 'FIT', 'FLU', 'FLY', 'FOE', 'FOG', 'FOR', 'FOX', 'FRY', 'FUN', 'FUR', 'GAD', 'GAG', 'GAL', 'GAM', 'GAP', 'GAS', 'GAT', 'GAY', 'GEL', 'GEM', 'GET', 'GIG', 'GIN', 'GOT', 'GUM', 'GUN', 'GUT', 'GUY', 'GYM', 'GYP', 'HAD', 'HAM', 'HAP', 'HAS', 'HAT', 'HAY', 'HEN', 'HER', 'HEY', 'HID', 'HIM', 'HIP', 'HIS', 'HIT', 'HOE', 'HOG', 'HOP', 'HOT', 'HOW', 'HUB', 'HUE', 'HUG', 'HUM', 'HUT', 'ICE', 'ICY', 'IDS', 'IFS', 'ILL', 'IMP', 'INK', 'INS', 'ION', 'IRE', 'IRK', 'ITS', 'IVY', 'JAB', 'JAG', 'JAM', 'JAR', 'JAW', 'JAY', 'JET', 'JEW', 'JIB', 'JIG', 'JIN', 'JOB', 'JOE', 'JOG', 'JOT', 'JOY', 'JUG', 'JUT', 'KEG', 'KEN', 'KEY', 'KID', 'KIN', 'KIT', 'LAB', 'LAD', 'LAG', 'LAM', 'LAP', 'LAW', 'LAY', 'LEA', 'LED', 'LEE', 'LEG', 'LET', 'LEU', 'LEY', 'LIB', 'LID', 'LIE', 'LIP', 'LIT', 'LOB', 'LOG', 'LOP', 'LOT', 'LOW', 'LYE', 'MAC', 'MAD', 'MAE', 'MAN', 'MAP', 'MAR', 'MAT', 'MAW', 'MAY', 'MEN', 'MET', 'MID', 'MIG', 'MIL', 'MOA', 'MOB', 'MOC', 'MOD', 'MOG', 'MOL', 'MOM', 'MON', 'MOO', 'MOP', 'MOR', 'MOT', 'MOW', 'MUD', 'MUG', 'MUM', 'NAB', 'NAG', 'NAH', 'NAN', 'NAP', 'NAW', 'NAY', 'NEB', 'NET', 'NEW', 'NIB', 'NIL', 'NIP', 'NIT', 'NIX', 'NOB', 'NOD', 'NOG', 'NOR', 'NOT', 'NOW', 'NUB', 'NUN', 'NUS', 'NUT', 'OAF', 'OAK', 'OAR', 'OAT', 'ODD', 'ODE', 'OFF', 'OFT', 'OHM', 'OIL', 'OLD', 'ONE', 'ONO', 'OOF', 'OPS', 'OPT', 'ORA', 'ORB', 'ORE', 'ORS', 'ORT', 'OUR', 'OUT', 'OVA', 'OWE', 'OWL', 'OWN', 'OXO', 'PAH', 'PAL', 'PAM', 'PAN', 'PAP', 'PAR', 'PAT', 'PAW', 'PAX', 'PAY', 'PEA', 'PEC', 'PED', 'PEE', 'PEG', 'PEH', 'PEN', 'PEP', 'PER', 'PET', 'PEW', 'PHI', 'PHT', 'PIA', 'PIC', 'PIE', 'PIG', 'PIN', 'PIP', 'PIS', 'PIT', 'PIU', 'PIX', 'PLY', 'POD', 'POH', 'POL', 'POM', 'POP', 'POT', 'POW', 'POX', 'PRY', 'PSI', 'PST', 'PUB', 'PUG', 'PUL', 'PUN', 'PUP', 'PUR', 'PUS', 'PUT', 'PYA', 'PYE', 'QUA', 'RAG', 'RAH', 'RAI', 'RAJ', 'RAM', 'RAN', 'RAP', 'RAT', 'RAW', 'RAX', 'RAY', 'REB', 'RED', 'REE', 'REF', 'REG', 'REI', 'REM', 'REP', 'RET']
# # dictionary = ['ABOUT', 'ABOVE', 'ACTOR', 'ADAPT', 'ADDED', 'ADMIR', 'ADOPT', 'ADULT', 'AFTER', 'AGAIN', 'AGENT', 'AGREE', 'ALARM', 'ALIVE', 'ALLOW', 'ALOHA', 'AMEND', 'ANGER', 'ANGLE', 'ANGRY', 'ANKLE', 'ANNEX', 'APPLE', 'APPLY', 'APRON', 'ARENA', 'ARGUE', 'ARISE', 'ARMED', 'ARROW', 'ASSET', 'ATTEM', 'AUDIO', 'AUNT', 'AUTH', 'AUTO', 'AVOID', 'AWARD', 'AWFUL', 'BABY', 'BAKE', 'BALD', 'BALL', 'BAND', 'BANK', 'BARE', 'BARK', 'BARN', 'BASE', 'BASH', 'BASK', 'BATH', 'BEAK', 'BEAM', 'BEAR', 'BEAT', 'BECK', 'BEEP', 'BEER', 'BEES', 'BEET', 'BELL', 'BELT', 'BEND', 'BEST', 'BETA', 'BETE', 'BETS', 'BIAS', 'BICE', 'BIDS', 'BIEN', 'BIKE', 'BILL', 'BIND', 'BIRD', 'BITE', 'BITS', 'BLACK', 'BLANK', 'BLAST', 'BLESS', 'BLOCK', 'BLOOD', 'BLOWS', 'BOARD', 'BOAST', 'BONUS', 'BOOST', 'BOOT', 'BOOTS', 'BOOTH', 'BORAD', 'BORDER', 'BORED', 'BOSSY', 'BOTCH', 'BOTH', 'BOUND', 'BOUT', 'BOWEL', 'BOWER', 'BOWIE', 'BOWLS', 'BOXER', 'BRAKE', 'BRAND', 'BRASS', 'BRAVE', 'BRAVO', 'BRAWS', 'BREAD', 'BREAK', 'BREED', 'BREWS', 'BRIEF', 'BRINE', 'BRINK', 'BROAD', 'BROIL', 'BROKE', 'BROWN', 'BRUSH', 'BUCKS', 'BULLS', 'BULLY', 'BUNCH', 'BURNT', 'BURST', 'BUSES', 'BUSTS', 'BUTTS', 'CABLE', 'CABOT', 'CACHE', 'CAFFE', 'CAGED', 'CAGES', 'CAKES', 'CALLS', 'CAMEL', 'CAMPS', 'CANDY', 'CANOE', 'CARBS', 'CARDS', 'CARRY', 'CASES', 'CASTS', 'CATCH', 'CATER', 'CATHY', 'CAVES', 'CELLS', 'CENTER', 'CEROS', 'CHAOS', 'CHARM', 'CHASE', 'CHEAP', 'CHECK', 'CHEER', 'CHEFS', 'CHIEF', 'CHILD', 'CHILI', 'CHINA', 'CHIPS', 'CHORD', 'CHUCK', 'CHURN', 'CIDER', 'CIGAR', 'CITED', 'CITES', 'CIVIC', 'CIVIL', 'CLAIM', 'CLAMP', 'CLANS', 'CLAPS', 'CLASH', 'CLASS', 'CLAWS', 'CLEAN', 'CLEAR', 'CLICK', 'CLIMB', 'CLIPS', 'CLOAK', 'CLOSE', 'CLOTH', 'CLOUD', 'CLOVE', 'CLOWN', 'CLUES', 'COACH', 'COAST', 'COATS', 'COCKS', 'CODER', 'CODES', 'COINS', 'COLAS', 'COLDS', 'COLOR', 'COMBO', 'COMET', 'COMIC', 'COMMA', 'COMBO', 'CONES', 'COOKS', 'COOLS', 'COOPS', 'COPED', 'COPES', 'CORES', 'CORNS', 'CORPS', 'CORPS', 'COUGH', 'COUNT', 'COUPE', 'COUPS', 'COURT', 'COVEN', 'COVER', 'COVES', 'COWLS', 'CRABS', 'CRACK', 'CRAFT', 'CRAMP', 'CRANE', 'CRANK', 'CRAVE', 'CRAZY', 'CREAM', 'CREWS', 'CRISP', 'CROCK', 'CROPS', 'CROSS', 'CROWD', 'CROWN', 'CRUDE', 'CRUEL', 'CRUSH', 'CRUST', 'CRYPT', 'CUBES', 'CUCUM', 'CUFFS', 'CULLS', 'CURBS', 'CURLS', 'CURLY', 'CURSE', 'CURVE', 'CUTER', 'CYCLE', 'DAISY', 'DAILY', 'DAIRY', 'DAISY', 'DALES', 'DAMEL', 'DAMPS', 'DANCE', 'DARED', 'DARES', 'DARKS', 'DARTS', 'DASHY', 'DATED', 'DATES', 'DAVID', 'DAWN', 'DAYSS', 'DEALS', 'DEALT', 'DEANS', 'DEARS', 'DEATH', 'DEBIT', 'DEBTS', 'DEBUG', 'DECAL', 'DECAY', 'DECOR', 'DECRY', 'DEEDS', 'DEEMS', 'DEEPS', 'DELAY', 'DELTA', 'DEMON', 'DENIM', 'DESKS', 'DEVIL', 'DIALS', 'DIARY', 'DICED', 'DICKS', 'DIDNT', 'DIGIT', 'DING']
# dictionary = ['ABANDONED', 'ABILITIES', 'ABOLISHED', 'ABOMINATE', 'ABORIGINAL', 'ABSCESSING', 'ABSORPTION', 'ABSURDNESS', 'ABUNDANTLY', 'ACCELERATE', 'ACCEPTANCE', 'ACCESSIBLE', 'ACCORDANCE', 'ACCRUEMENT', 'ACETYLENES', 'ACHIEVABLE', 'ACQUITTALS', 'ACTIVATING', 'ADAPTATION', 'ADDRESSING', 'ADHERENTLY', 'ADJACENTLY', 'ADJUSTABLE', 'ADJUSTMENT', 'ADMISSIBLE', 'ADMONITION', 'ADOPTIVELY', 'ADULATION', 'ADVENTURES', 'ADVERTISED', 'ADVERTIZES', 'ADVISABLES', 'AESTIVATED', 'AFFIRMABLE', 'AFFLICTIVE', 'AFFLUENTLY', 'AFORETHOUGHT', 'AGGRAVATED', 'AGITATEDLY', 'ALCOHOLICS', 'ALLITERATE', 'ALLOCATION', 'ALLOWANCES', 'ALMSGIVING', 'ALPHABETIC', 'ALTERATION', 'AMBIVALENT', 'AMENORRHEA', 'AMPHIBIOUS', 'ANALOGICAL', 'ANATOMICALLY', 'ANCHORAGES', 'ANGULARITY', 'ANNIHILATE', 'ANNOUNCING', 'ANOMALISTS', 'ANTAGONISM', 'ANTECEDENT', 'ANTICIPATE', 'APPEARANCE', 'APPEASABLE', 'APPLICABLE', 'APPOINTEES', 'APPOSITION', 'APPRAISERS', 'APPRECIATE', 'APPROVABLE', 'APPROXIMAL', 'ARCHAICISM', 'ARCHITECTS', 'ARDUOUSNESS', 'ARRAIGNING', 'ARRANGEMENT', 'ARROGANTLY', 'ARTICULATED', 'ARTIFICIAL', 'ASCENDANTS', 'ASCENDENTS', 'ASCERTAINS', 'ASPERITIES', 'ASSEMBLERS', 'ASSEMBLIES', 'ASSEMBLAGE', 'ASSESSABLE', 'ASSESSMENT', 'ASSIMILATE', 'ASSISTANTS', 'ASSOCIATED', 'ASTONISHED', 'ASTRONOMER', 'ASTRONOMIC', 'ATHLETICAL', 'ATMOSPHERE', 'ATTACHABLE', 'ATTAINABLE', 'ATTEMPTING', 'ATTENDANCE', 'ATTENUATED', 'ATTRACTIVE', 'AUCTIONING', 'AUDITIONED', 'AUSTERENESS', 'AUTHORIZES', 'AUTHORIZED', 'AUTONOMOUS', 'AUTONOMICS', 'AUTOMATION', 'AUTOMATONS', 'AVAILABLY', 'AVERTABLE', 'AWARENESS', 'BACKFIRED', 'BACKWARDS', 'BALLOONED', 'BANISHING', 'BANKRUPTC', 'BANKRUPTED', 'BAPTIZING', 'BARRICADE', 'BASICALLY', 'BEFITTING', 'BEGUILING', 'BELIEVING', 'BEMOANING', 'BENCHMARK', 'BENEVOLEN', 'BEREAVING', 'BESIEGING', 'BESTOWING', 'BEWAILING', 'BEWITCHIN', 'BICYLEING', 'BIFURCATI', 'BIRTHDAYS', 'BITTERNESS', 'BLASPHEMY', 'BLASPHEMY', 'BLENDINGS', 'BLINDNESS', 'BLISTERIN', 'BLOCKINGS', 'BLOODYING', 'BLOSSOMED', 'BLOTTINGS', 'BOASTFULL', 'BODYBUILD', 'BODYGUARD', 'BOLSTERED', 'BORDERING', 'BORROWING', 'BOUQUETED', 'BOWSTRUNG', 'BRACKETED', 'BRANCHING', 'BREACHING', 'BREASTING', 'BRIDGINGS', 'BRILLIANT', 'BROADCAST', 'BRONCHITI', 'BROWSINGS', 'BUCCANEER', 'BUILDSUPS', 'BULGINGLY', 'BULLDOZER', 'BULLDOZED', 'BURDENING', 'BURGLARIE', 'BUSHINESS', 'BUTTERING', 'BUTTONING', 'CALCULATE', 'CANDLELIT', 'CANDYGRAM', 'CANNIBALS', 'CANNOTMIS', 'CANTATAS', 'CANTONING', 'CARNALITY', 'CARPETING', 'CASHIERED', 'CASTIGATE', 'CATALOGUE', 'CATEGORIC', 'CAVITATED', 'CELEBRATE', 'CENSORING', 'CENTRALLY', 'CEREBRALS', 'CHALLENGE', 'CHALLENGE', 'CHAPERONE']

# trie = Trie()

# for word_trie in dictionary:
#     trie.insert_word(word=word_trie)

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

    
        
        