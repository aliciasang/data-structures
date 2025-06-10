import random
import time
import sys

def findOperandsList1(list_: list[int], k: int) -> bool:
    ''' function to determine whether two entries in the list sum to k
    Parameter:
        list_: a list of integers
        k: an integer
    Returns:
        True if two sum to k, False o/w
    '''
    # use list processing only -- do not use a new/separate list or 
    # a dictionary
    for i in range(len(list_)):
        for j in range(i + 1, len(list_)):
            if list_[i] + list_[j] == k:
                return True
    return False

def findOperandsDict(list_: list[int], k: int) -> bool:
    ''' function to determine whether two entries in the list sum to k
    Parameter:
        list_: a list of integers
        k: an integer
    Returns:
        True if two sum to k, False o/w
    '''
    # use a dictionary to solve the problem in O(n) time -- do not
    # use a separate list
    seen = {} # seen = {value, index}
    for num in list_:
        if k - num in seen:
            return True
        seen[num] = True
    return False
   
    
def findOperandsList2(list_: list[int], k: int) -> bool:
    ''' function to determine whether two entries in the list sum to k
    Parameter:
        list_: a list of _nonegative_ integers
        k: a _nonnegative_ integer
    Returns:
        True if two sum to k, False o/w
    '''
    # similar to the dictionary approach but use a separate list (not a
    # dictionary) to solve the problem... what are the constraints?
    if k < 0:
        raise ValueError("False: two non-negative integers cannot sum to a negative")
    
    seen = [False] * (k + 1)
    for num in list_:
        if 0 <= k - num <= k and seen[k - num]:
            return True
        if num <= k:
            seen[num] = True
    return False
    
def main() -> None:
    print("Running tests to check that all three functions actually work")

    print("findOperandsList1 tests")
    assert findOperandsList1([1, 2, 3, 4], 5) == True     # 2 + 3 = 5
    assert findOperandsList1([1, 2], 4) == False          # nothing adds to 4
    assert findOperandsList1([5, 5], 10) == True          # two of the same value works

    print("findOperandsDict tests")
    assert findOperandsDict([1, 2, 3, 4], 5) == True      # same as above, but dictionary-based
    assert findOperandsDict([1, 2], 4) == False
    assert findOperandsDict([5, 5], 10) == True

    print("findOperandsList2 tests")
    assert findOperandsList2([1, 2, 3, 4], 5) == True
    assert findOperandsList2([1, 2], 4) == False
    assert findOperandsList2([5, 5], 10) == True

    print("All tests passed\n")

    # now testing on a big randomly generated list to compare performance
    random.seed(8675309)
    max_val = 10000
    list_size = 10000
    look_for = max_val

    l = [random.randint(1, max_val) for _ in range(list_size)]

    start = time.perf_counter()
    result = findOperandsList1(l, look_for)
    end = time.perf_counter()
    print(f"using list analysis: {result} found in {end - start:.6f} seconds")

    start = time.perf_counter()
    result = findOperandsDict(l, look_for)
    end = time.perf_counter()
    print(f"using dictionary:    {result} found in {end - start:.6f} seconds")

    start = time.perf_counter()
    result = findOperandsList2(l, look_for)
    end = time.perf_counter()
    print(f"using separate list: {result} found in {end - start:.6f} seconds")

if __name__ == "__main__":
    main()
