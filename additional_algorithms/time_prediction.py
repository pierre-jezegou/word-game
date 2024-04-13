'''Compute theorical model of number of sub-words generated by a word
    Print (x, y) couples for 
'''
import math

MAX_LENGTH = 25
MIN_LENGTH = 3

def complexity(m: int, k: int) -> int:
    '''Gives the number of combination'''
    return math.factorial(m) // (math.factorial(k) * math.factorial(m - k))

def total_combination(m:int , min_length:int =3) -> int:
    '''Sum combinations for all allowed word lengths'''
    counter = 0
    for i in range(min_length, m):
        counter += complexity(m, i)
    return counter

def main():
    '''Main function'''
    letters_length = list(range(MIN_LENGTH, MAX_LENGTH))
    counters = [total_combination(i) for i in letters_length]

    for i in range(len(letters_length)):
        print(f"(%s, %s)" % (letters_length[i], counters[i]))

if __name__=="__main__":
    main()