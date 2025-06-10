'''
References:
Progress bar documentation: https://pypi.org/project/progress/
'''

from List import *
from progress.bar import Bar
import time
import random

################################################################################
def oneExperiment(list_size: int, prob_remove: float = 0.0, growth_type: str = 'fixed', growth_value: int | float = 2) -> dict[str, int]:
    ''' function to conduct one experiment by creating a List object,
        then appending list_size number of integers, with each integer chosen
        at random between 1 and 1000 both inclusive
    Parameters:
        list_size: the size of the List to be created
        prob_remove: probability of removing a random item immediately after
            a new append (i.e., whether, after just appending an item, to
            remove a randomly-selected different item that exists in the list)
    Returns:
        a dictionary of post-experiment stats (see List.py):
            - 'capacity': the resulting internal array capacity (filled and empty)
            - 'resizes': the number of array resizes required across all appends
            - 'append_copies': the number of array-to-array items copied across all appends
            - 'remove_copies': the number of array-to-array items copied as a result of removes 
    '''
    l = List(growth_type = growth_type, growth_value = growth_value)

    for i in range(list_size):
        random_integer = random.randint(1, 999999)
        l.append(random_integer)

        if random.random() < prob_remove and len(l) > 0:
            random_index = random.randint(0, len(l) - 1)
            item_remove = l[random_index]
            l.remove(item_remove)
    
    return l.getInternalStats()

################################################################################
def main() -> None:
    random.seed(8675309)
    list_sizes_no_remove   = [10**4, 10**5, 10**6] #, 10**7]
    list_sizes_with_remove = [10**4, 10**5, 10**6]

    num_experiments_per = 3
    
    #list_sizes = list_sizes_no_remove   # or = list_sizes_with_remove / use references to our advantage in loop below
    list_sizes = list_sizes_with_remove
    prob_remove = 1 / 1000

    growth_tests = [
        ('relative', 2),
        ('relative', 1.5),
        ('fixed', 1024),
        ('fixed', 8192),
        ('fixed', 32768)
    ]

    for growth_type, growth_value in growth_tests:
        print("=" * 50)
        print(f"Growth_type={growth_type}, growth_value={growth_value}, prob_remove={prob_remove}")
        print("=" * 50)

        for list_size in list_sizes:
            if list_size == 10**7 and not ((growth_type == 'relative' and growth_value == 2) or (growth_type == 'fixed' and growth_value == 1024)): # only run appropriate experiments for 10^7
                continue

            print(f'Experimenting with list size {list_size}')
            total_time = 0
            total_capacity = 0
            total_resizes = 0
            total_append_copies = 0
            total_remove_copies = 0

            bar = Bar('Running experiments', max = num_experiments_per)

            for i in range(num_experiments_per):
                start_time = time.process_time()
                stats = oneExperiment(list_size, prob_remove = prob_remove, growth_type = growth_type, growth_value = growth_value)
                end_time = time.process_time()

                total_time += (end_time - start_time)
                total_capacity += stats['capacity']
                total_resizes += stats['resizes']
                total_append_copies += stats['append_copies']
                total_remove_copies += stats['remove_copies']

                bar.next()
            bar.finish()

            average_time = total_time / num_experiments_per
            average_capacity = total_capacity / num_experiments_per
            average_resizes = total_resizes / num_experiments_per
            average_append_copies = total_append_copies / num_experiments_per
            average_remove_copies = total_remove_copies / num_experiments_per

            print(f"Average Time: {average_time:.4f} seconds")
            print(f"Average Capacity: {average_capacity}")
            print(f"Average Resizes: {average_resizes}")
            print(f"Average Append Copies: {average_append_copies}")
            print(f"Average Remove Copies: {average_remove_copies}")

if __name__ == "__main__":
    main()