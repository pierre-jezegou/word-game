'''Simulate word challenge'''
import sys
import time
import json
from prettytable import PrettyTable
import numpy as np
from tries import Trie
from additional_algorithms.string_words_manipulation import *
from set_dictionary import *

def automated_mode(trie: Trie, length: int = 0):
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
        if length != 0:
            while len(letters) != length:
                letters = get_random_shuffled_list("dictionary.txt")

        start_time = time.time()
        # word_counter = 0
        word_counter, _ = trie.word_game_main_function(letters)
        end_time = time.time()
        elapsed_time = end_time - start_time
        results.append({
            "iteration": i,
            "initial_word_length": len(letters),
            "cpu_time": elapsed_time,
            "word_counter": word_counter,
        })
    return results


def manual_mode(trie: Trie, given_letters: str) -> list[dict[int|float]]:
    '''Simulate x times word_challenge (x given by user in cmd line)'''

    results : list[dict[int|float]] = []

    start_time = time.time()
    word_counter, _ = trie.word_game_main_function(given_letters)
    end_time = time.time()

    elapsed_time = end_time - start_time
    results.append({
        "iteration": 1,
        "initial_word_length": len(given_letters),
        "cpu_time": elapsed_time,
        "word_counter": word_counter,
    })
    return results

def print_results_in_table(results: list[dict[int|float]]) -> None:
    '''Print results in pretty table'''
    table = PrettyTable(["Iteration", "Initial length", "CPU time", "Word counter"])
    len_results = len(results)
    for i, result in enumerate(results):
        table.add_row([result["iteration"],
                       result["initial_word_length"] ,
                       result["cpu_time"],
                       result["word_counter"]
                       ],
                       divider = i == len_results - 1)

    mean_cpu_time = np.mean([result["cpu_time"] for result in results])
    mean_word_counter = np.mean([result["word_counter"] for result in results])
    table.add_row(["AVG:", None,mean_cpu_time, mean_word_counter])
    print(table)




# class Test():
#     '''Implementation of a test measures'''
#     def __init__(self,
#                  test_iteration: int,
#                  cpu_time: float,
#                  word_count: float,
#                  length: int):

#         self.cpu_time: float    = cpu_time
#         self.word_count: float  = word_count
#         self.length: int        = length
#         self.test_iteration     = test_iteration


# def _display_performances(samples: int) -> None:
#     # results: list[dict[int|float]] = []
#     results: list[Test] = []
#     for i in range(samples):
#         letters = get_random_shuffled_list("dictionary.txt")
#         start_time = time.time()
#         a = 10**len(letters)
#         end_time = time.time()
#         elapsed_time = end_time - start_time

#         results.append(Test(i,
#                             elapsed_time,
#                             0, # TODO Change when game ready to return counter
#                             len(letters)))

#     processed_results = {i: {
#                            "cpu_time": [result.cpu_time for result in results if result.length == i],
#                            "word_count": [result.word_count for result in results if result.length == i],
#                            } for i in [result.length for result in results]}

#     # labels = [processed_results[i]["length"] for i in [result.length for result in results]]
#     lengths = [result.length for result in results]
#     mean_cpu_time = [np.mean(processed_results[i]["cpu_time"]) for i in [result.length for result in results]]
#     mean_word_count = [np.mean(processed_results[i]["word_count"]) for i in [result.length for result in results]]

#     plt.figure()
#     plt.scatter(lengths, mean_cpu_time, label="CPU time")
#     plt.scatter(lengths, mean_word_count, label="Word count")
#     plt.legend()
#     plt.show()

#     print(processed_results)

def save_results_json(results:list[dict[str|float]]) -> None:
    with open('exports/results_'+str(time.time())+".json", 'w') as f:
        json.dump(results, f, indent=4)



MODE_AUTO = True

if __name__ == "__main__":
    trie = build_trie('dictionary.txt')
    if MODE_AUTO:
        results = automated_mode(trie)
    else:
        results = manual_mode(trie, ['f', 'o', 'r', 'c', 'e'])
    save_results_json(results)
    print_results_in_table(results)