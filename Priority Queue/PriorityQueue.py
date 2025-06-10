from __future__ import annotations

import copy   # for using deepcopy
import heapq
import random
import string

############################
class EmptyError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message

#################
class Entry[K,V]:
    __slots__ = ('key', 'value')

    def __init__(self, priority: K, data: V) -> None:
        self.key  : K = priority
        self.value: V = data

    def __str__(self) -> str:
        ''' returns a string representation of this key:value Entry
        Returns:
            string version of this Entry
        '''
        return f"({self.key},{self.value})"

    def __lt__(self, other: Entry[K,V]) -> bool:
        ''' determines whether this Entry is less than another Entry
        Parameters:
            other: a separate Entry object
        Returns:
            True if this's key is less than other's key, or
                if this's key and other's key are the same while
                   this's value is less than other's value
        '''
        return self.key < other.key

    # not the Pythonic way to use __repr__ but allows us to print a list of Entry
    def __repr__(self) -> str: 
        return f"({repr(self.key)},{'∅' if self.value is None else repr(self.value)})"

#######################
class PriorityQueue[K,V]:
    __slots__ = ('_container')

    def __init__(self) -> None:
        self._container: list[Entry[K,V]] = list()

    def __len__(self)  -> int:  return len(self._container)
    def isEmpty(self) -> bool:  return len(self._container) == 0

    def insert(self, key: K, item: V) -> None: 
        ''' method to create a new Entry having key (e.g., time) and
            item (e.g., event to occur at that time),  and then insert the
            Entry into the heap (self._container) using heapq.heappush
        Parameters:
            key: the entry's priority
            item: the entry's data
        '''
        entry = Entry(key, item)
        heapq.heappush(self._container, entry)

    def removeMin(self) -> Entry[K,V]:
        ''' method to remove the highest priority (e.g., minimum time) Entry
            from the PriorityQueue, returning that Entry
        Returns:
            Entry object corresponding to the highest priority Entry
        Raises:
            EmptyError if the priority queue is empty
        '''
        if self.isEmpty():
            raise EmptyError("Priority Queue is empty")
        return heapq.heappop(self._container)

    def min(self) -> Entry[K,V]:
        ''' method to return but not remove the highest priority (e.g., minimum
            time) Entry from the PriorityQueue, returning that Entry
        Returns:
            a copy of the Entry object corresponding to the highest priority
            Entry
        Raises:
            EmptyError if the priority queue is empty
        '''
        if self.isEmpty():
            raise EmptyError("Priority Queue is empty")
        return self._container[0]
    
    def __str__(self) -> str:
        return str(self._container)

########################## need to work on this
def main() -> None:
    pq = PriorityQueue()
    print(f"len of pq = {len(pq)}")
def main() -> None:
    pq = PriorityQueue()

    print("Testing PriorityQueue")

    print("Initial State")
    print(f"Expected length: 0 | Actual: {len(pq)}")
    print(f"Expected isEmpty: True | Actual: {pq.isEmpty()}")

    print("\nInserting Elements")
    pq.insert(5, "event at 5")
    pq.insert(3, "event at 3")
    pq.insert(4, "event at 4")
    pq.insert(1, "event at 1")
    pq.insert(2, "event at 2")

    print("\nInternal Heap Structure")
    print("Expected: Valid min-heap structure (by priority)")
    print("Actual:", [str(e) for e in pq._container])

    print("\nTesting min()")
    print(f"Expected: event at 1 | Actual: {pq.min()}")

    print("\n-- Removing Elements in Priority Order --")
    expected_order = [
        "event at 1",
        "event at 2",
        "event at 3",
        "event at 4",
        "event at 5",
    ]
    for expected in expected_order:
        actual = pq.removeMin()
        print(f"Expected: {expected} | Actual: {actual}")

    print("\nFinal State")
    print(f"Expected isEmpty: True | Actual: {pq.isEmpty()}")
    print(f"Expected length: 0 | Actual: {len(pq)}")

if __name__ == "__main__":
    main()