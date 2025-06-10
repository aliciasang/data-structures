from __future__ import annotations
from EmptyError import EmptyError
from typing import TypeVar, Generic

class Node[T]:
    ''' class to implement a single node object in a singly-linked
        linked list '''
    __slots__ = ('data', 'next', 'prev')

    def __init__(self, data: T):
        self.data: T       = data
        self.next: Node[T] = None
        self.prev: Node[T] = None

class LinkedList[T]:
    ''' class to implement a doubly-linked linked list '''
    def __init__(self) -> None:
        self._head: Node[T] = None
        self._tail: Node[T] = None
        self._size: int     = 0

    def __len__(self) -> int:
        ''' returns the number of elements in the linked list
        Returns:
            int: the number of elements in the list'''
        return self._size

    def appendLeft(self, item: T) -> None:
        ''' append the given T-type data item as part of a new Node to the left
            side of the linked list
        Parameters:
            item: a type T data item to be included as the data in the inserted Node
        Returns:
            nothing
        '''
        if self._size > 0 and not isinstance(item, type(self._head.data)):
            raise TypeError("LinkedList requires consistent types")
        else:
            new_node = Node(item)
            new_node.next = self._head
            if self._head is not None:
                self._head.prev = new_node
            self._head = new_node

            if self._size == 0:
                self._tail = new_node
            self._size += 1

    def appendRight(self, item: T) -> None:
        ''' appends the given T-type data item as part of a new Node to the right 
            of the linked list
        Parameters:
            item: a type T data item to be included as the data in the inserted Node
        Returns:
            nothing
        '''
        if self._size > 0 and not isinstance(item, type(self._tail.data)):
            raise TypeError("LinkedList requires consistent types")
        else:
            new_node = Node(item)
            if self._tail is not None:
                self._tail.next = new_node
                new_node.prev = self._tail
            self._tail = new_node

            if self._size == 0:
                self._head = new_node
            self._size += 1

    def popLeft(self) -> T:
        ''' removes the first Node in the linked list, returning the data item
            inside that Node
        Returns:
            a T type data item extracted from the removed Node
        Raises:
            EmptyError exception if list is empty
        '''
        if self._size == 0:
            raise EmptyError("Cannot popLeft from an empty list")

        value = self._head.data

        if self._head == self._tail:
            self._head = self._tail = None
        else:
            self._head = self._head.next
            self._head.prev = None
        self._size -= 1
        return value
    

    def popRight(self) -> T:
        ''' removes the last Node in the linked list, returning the data item
            inside that Node
        Returns:
            a T type data item extracted from the removed Node
        Raises:
            EmptyError exception if list is empty
        '''
        if self._size == 0:
            raise EmptyError("Cannot popRight from an empty list")

        value = self._tail.data

        if self._head == self._tail:
            self._head = self._tail = None
        else:
            self._tail = self._tail.prev
            self._tail.next = None  
        self._size -= 1
        return value

    def __str__(self):
        ''' returns a str representation of the linked list data
        Returns:
            an str representation of the linked list, showing head pointer
                and data items
        '''
        result = "head->"
        ptr = self._head 
        while ptr is not None:
            result += f"[{str(ptr.data)}]<->"
            ptr = ptr.next
        if self._size > 0:
            result = result[:-3]
        result += "<-tail"
        return result
    
    def front(self) -> T:
        ''' returns data at the head of the list without removing it
        Returns:
            T: the data stored in the head node
        Raises:
            EmptyError: if the list is empty'''
        if self._head is None:
            raise EmptyError("Linked List is empty")
        return self._head.data
    
    def back(self) -> T:
        '''returns data at the tail of the list without removing it
        Returns:
            T: the data stored in the tail node
        Raises:
            EmptyError: if the list is empty
        '''
        if self._tail is None:
            raise EmptyError("Linked List is empty")
        return self._tail.data

def main():
    print("Testing LinkedList")
    l = LinkedList[int]()
    print("Is empty?", len(l) == 0)

    print("testing appendLeft x4")
    l.appendLeft(3)
    l.appendLeft(2)
    l.appendLeft(1)
    l.appendLeft(0)
    print("After appendLeft x4:", l)

    print("Testing front and back")
    print("Front:", l.front())
    print("Back:", l.back())

    print("Testing popLeft x2")
    print("PopLeft:", l.popLeft())
    print("PopLeft:", l.popLeft())
    print("List after popLeft x2:", l)

    print("Testing appendRight x4")
    l.appendRight(4)
    l.appendRight(5)
    l.appendRight(6)
    l.appendRight(7)
    print("After appendRight x4:", l)

    print("Testing front and back")
    print("Front again:", l.front())
    print("Back again:", l.back())

    print("Testing popRight x4")
    print("popRight:", l.popRight())
    print("popRight:", l.popRight())
    print("popRight:", l.popRight())
    print("popRight:", l.popRight())
    print("List after popRight x4:", l)

if __name__ == "__main__":
    main()