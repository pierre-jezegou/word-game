'''Simulate word challenge'''
import re
import random
import sys
import time
from prettytable import PrettyTable
import numpy as np
import matplotlib.pyplot as plt

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
                return line.strip()
    raise IndexError


def get_random_shuffled_list(file_path: str) -> list:
    '''Compose get_line and shuffle word to get a random shuffled word'''
    string = extract_informations(get_random_line(file_path))
    return list(shuffle_string(string))


def automated_mode():
    '''Simulate x times word_challenge (x given by user in cmd line)'''
    try:
        number_times_needed = int(sys.argv[1])
    except IndexError:
        raise IndexError("Usage : python word_challenge.py <argument:int>")
    except ValueError:
        raise ValueError("Send int")

    results : list[dict[int|float]] = []

    for i in range(number_times_needed):
        letters = get_random_shuffled_list("dictionary.txt")

        start_time = time.time()
        #ACTIONS
        end_time = time.time()
        elapsed_time = end_time - start_time
        results.append({
            "iteration": i,
            "cpu_time": elapsed_time,
            "word_counter": 0,
        })
    return results


def print_results_in_table(results: list[dict[int|float]]) -> None:
    '''Print results in pretty table'''
    table = PrettyTable(["Iteration", "CPU time", "Word counter"])
    len_results = len(results)
    for i, result in enumerate(results):
        table.add_row([result["iteration"], 
                       result["cpu_time"],
                       result["word_counter"]
                       ],
                       divider = i == len_results - 1)

    mean_cpu_time = np.mean([result["cpu_time"] for result in results])
    mean_word_counter = np.mean([result["word_counter"] for result in results])
    table.add_row(["AVG:", mean_cpu_time, mean_word_counter])
    print(table)




class Test():
    '''Implementation of a test measures'''
    def __init__(self,
                 test_iteration: int,
                 cpu_time: float,
                 word_count: float,
                 length: int):
        
        self.cpu_time: float    = cpu_time
        self.word_count: float  = word_count
        self.length: int        = length
        self.test_iteration     = test_iteration




def _display_performances(samples: int) -> None:
    # results: list[dict[int|float]] = []
    results: list[Test] = []
    for i in range(samples):
        letters = get_random_shuffled_list("dictionary.txt")
        start_time = time.time()
        a = 10**len(letters)
        end_time = time.time()
        elapsed_time = end_time - start_time

        results.append(Test(i,
                            elapsed_time,
                            0, # TODO Change when game ready to return counter
                            len(letters)))
    
    processed_results = {i: {
                           "cpu_time": [result.cpu_time for result in results if result.length == i],
                           "word_count": [result.word_count for result in results if result.length == i],
                           } for i in [result.length for result in results]}
    
    # labels = [processed_results[i]["length"] for i in [result.length for result in results]]
    lengths = [result.length for result in results]
    mean_cpu_time = [np.mean(processed_results[i]["cpu_time"]) for i in [result.length for result in results]]
    mean_word_count = [np.mean(processed_results[i]["word_count"]) for i in [result.length for result in results]]

    plt.figure()
    plt.scatter(lengths, mean_cpu_time, label="CPU time")
    plt.scatter(lengths, mean_word_count, label="Word count")
    plt.legend()
    plt.show()
    
    print(processed_results)

if __name__ == "__main__":
    # results = automated_mode()
    # print_results_in_table(results)
    res = _display_performances(10**4)
    print(res)

# b = [[result_grouped["length"] for result_grouped in a if result_grouped["length"] == i] for i in [result["length"] for result in a]]