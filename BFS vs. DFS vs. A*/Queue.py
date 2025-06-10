from typing import TypeVar
from collections import deque

T = TypeVar("T")

class EmptyError(Exception):
    ''' class extending Exception to better document queue errors '''
    def __init__(self, message: str):
        self.message = message

class Queue[T]:
    __slots__ = ('_data',)

    def __init__(self)	-> None:	
        '''initializes item of empty Queue class'''
        self._data = deque()
        
    def push(self, element: T) 	-> None: # FIFO
        '''add an element to the end of the list
        Args:
            element: the element to be added to the end of the list
        Returns: 
            None
        Raises: 
            TypeError: if element is not an integer
        '''
        self._data.append(element)

    def pop(self) -> T: # FIFO
        '''removes and returns the first element of a list
        Args: 
            the queue
        Returns:
            T: the value removed from the front of the queue
        Raises:
            Error: if queue is empty'''
        if self.isEmpty():
            raise EmptyError('Error: pop() cannot be executed on an empty queue')
        return self._data.popleft()
    
    def top(self)-> T:	
        '''returns the front element of a list, without removing it
        Args:
            The queue
        Returns:
            T: the data from the front element of the queue
        Raises:
            Error: if queue is empty'''
        if self.isEmpty():
            raise EmptyError('Error: no top of an empty list')
        return self._data[0]
    
    def isEmpty(self) -> bool: 
        '''Determines if queue is empty
        Args: 
            Queue
        Returns: 
            True if queue is empty, else false'''
        return len(self._data) == 0
    
    def __len__(self) -> int:
        '''return the number of elements in the queue
        Args: 
            Queue
        Returns: 
            int: length of queue
        
        '''
        return len(self._data)
    
    def __str__(self) -> str:	
        return str(list(self._data))
        
def main() -> None:
    queue = Queue[int]()
    
    print('\nTesting .push()')
    queue.push(1)
    queue.push(4)
    queue.push(7)
    print(f'  Actual: {queue}')
    print(f'Expected: [1, 4, 7]\n')
    
    print('Testing .top')
    print(f'  Actual: {queue.top()}')
    print(f'Expected: 1\n')

    print('Testing .pop')
    queue.pop()
    print(f'  Actual: {queue}')
    print(f'Expected: [4, 7]\n')
    queue.pop()
    queue.pop()

    print('Testing .isEmpty()')
    print(f'  Actual: {queue.isEmpty()}')
    print(f'Expected: True\n')

    print('Testing __str__')
    print(f'  Actual: str(queue)')
    print(f'Expected: []\n')

    print('Testing __len__')
    print(f'  Actual: {queue.__len__()}')
    print(f'Expected: 0\n')

if __name__ == "__main__":
    main()