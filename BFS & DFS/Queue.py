from __future__ import annotations
from EmptyError import EmptyError
from LinkedList import LinkedList
from typing import TypeVar, Generic

T = TypeVar('T')

class Queue(Generic[T]):
    def __init__ (self):
        ''' Initializes an empty queue using a linked list'''
        self._data = LinkedList[T]()
    
    def __len__ (self) -> int:
        '''returns the number of items in the queue
        Returns:
            int: indicates the number of items in the queue
        '''
        return len(self._data)
    
    def isEmpty (self) -> bool:
        '''indicates if the queue is empty
        Returns:
            bool: True if the queue is empty, False otherwise
        '''
        return len(self._data) == 0
    
    def push(self, item: T) -> None:
        '''inserts the given item at the end of the queue
        Parameters:
            item: the item to be inserted
        Raises:
            TypeError if the given item is not of the same type as the existing items
        '''
        if self._data._size > 0 and not isinstance(item, type(self.top())):
            raise TypeError("Queue requires consistent types")
        else:
            self._data.appendRight(item)

    def pop(self) -> T:
        '''removes and returns item at the front of the queue
        Returns:
            T: item at the front of the queue
        Raises:
            EmptyError if the queue is empty
        '''
        if self.isEmpty():
            raise EmptyError("Cannot pop from an empty queue")
        return self._data.popLeft()

    def top(self) -> T:       
        '''returns the item at the front of the queue without removing it
        Returns:
            T: item at the front of the queue
        Raises:
            EmptyError if the queue is empty
        '''
        if self.isEmpty():
            raise EmptyError("Cannot top an empty queue")
        return self._data.front()
    
    def __str__(self):
        '''returns a string representation of the queue
        Returns:
            str: a string representation of the queue showing its elements
        '''
        return str(self._data)

class Node:
    def __init__(self, data):
        '''initializes a Node with the given data
        Parameters:
            data: The data to be stored in the Node.
        '''
        self.data = data
        self.next = None

    def __str__(self):    
        '''returns a string representation of the node's data
        Returns:
            str: a string representation of the data contained in the node'''
        return str(self.data)
    
def main():
    q = Queue[int]()
    print(f"Empty?    {q.isEmpty()}")
    print(f"Expected: True\n")

    q.push(1)
    q.push(2)
    q.push(3)
    q.push(4)

    print(f"Top:  {q.top()}")
    print("Expected: 1\n")

    print(f"Pop:     {q.pop()}")
    print("Expected: 1\n")

    print(f"Top after pop: {q.top()}")
    print("Expected:       2\n")

    print(f"Length:  {len(q)}")
    print("Expected: 3\n")

    print(f"Pop: {q.pop()}")
    print(f"Pop: {q.pop()}")
    print(f"Pop: {q.pop()}")

    print("\nIs empty after pops?")
    print(f"Result:   {q.isEmpty()}")
    print(f"Expected: True\n")

    try:
        q.pop()
    except EmptyError as e:
        print(f"Pop from empty: Exception caught")
        print(f"Expected:       Exception caught\n")

    try:
        q.top()
    except EmptyError as e:
        print(f"Top from empty: Exception caught")
        print(f"Expected:       Exception caught")

if __name__ == "__main__":
    main()