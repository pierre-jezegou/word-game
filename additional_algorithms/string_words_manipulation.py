''' Aim of this file :
    - Manipulate strings and lists to extract usefull data
    - Shuffle strings
'''
import random
import re


REGEX_TEXT = r'^(?:[a-zA-Z]+)'
REGEX_COUNTER = r'(\d+)'


def extract_informations(text: str) -> dict[str|int] | None:
    '''Extract text and counter from a given string
        Ex: extract str:"abbey" and int:4224864 from "abbey:4224864"'''

    extracted_text = re.match(REGEX_TEXT, text)

    return extracted_text.group()
    # extracter_counter = re.match(REGEX_COUNTER, text)
    # if extracted_text and extracter_counter:
    #     return {
    #         "text": extracted_text,
    #         "counter": int(extracter_counter.group())
    #     }


def shuffle_string(string: str) -> str:
    '''Random shuffle of a string'''
    print(string)
    tmp = list(string)
    random.shuffle(tmp)
    return ''.join(tmp)

def get_random_line(file_path: str) -> str:
    '''Get random line from a goven file'''

    with open(file_path, 'r') as file:
        num_lines = sum(1 for line in file)
        random_line_num = random.randint(0, num_lines - 1)

        file.seek(0)

        for line_number, line in enumerate(file):
            if line_number == random_line_num:
                return line.strip().split(':')[0]
    raise IndexError


def get_random_shuffled_list(file_path: str) -> list:
    '''Compose get_line and shuffle word to get a random shuffled word'''
    string = extract_informations(get_random_line(file_path))
    return list(shuffle_string(string))