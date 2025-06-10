import sys
import time
import random
from typing import Tuple

def parse_args() -> Tuple[int, int, str, int]:
    '''Parses command-line arguments and checks for errors'''
    try:
        replications = int(sys.argv[1])
        appends = int(sys.argv[2])
        append_option = sys.argv[3]
        seed = int(sys.argv[4])
        
        if len(sys.argv) != 5: # argv separates command line args by spaces
            raise SyntaxError('Usage: python hw4.py [# replications] [# appends][append option: (a) .append (b) += (c) +]  [seed]')

        if append_option not in ('a', 'b', 'c'):
            raise ValueError('Invalid append option')

    except ValueError:
        print("Invalid input. # of replications, # of appends, and seed must be integers. Append option must be strings 'a', 'b', or 'c'.")
        sys.exit(0)

    return replications, appends, append_option, seed

def time_append(replications: int, appends: int, append_option: str, seed: int) -> float:
    '''Runs a timing test for the three different list append methods'''
    random.seed(seed)
    total_time = 0.0

    for i in range(replications):
        my_list = []
        start = time.process_time()

        for j in range(appends):
            new_int = random.randint(1, 999999)

            if append_option == 'a':
                my_list.append(new_int)
            elif append_option == 'b':
                my_list += [new_int]
            else: # must be c
                my_list = my_list + [new_int]

        total_time += time.process_time() - start

    return total_time / replications

def main() -> None:
    replications, appends, append_option, seed = parse_args()
    avg_time = time_append(replications, appends, append_option, seed)

    print(f"Seed: {seed} \n Replications: {replications} \n Appends: {appends}")
    print(f"Average time using append option '{append_option}' is {avg_time:.4f} seconds")

if __name__ == "__main__":
    main()