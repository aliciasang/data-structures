from __future__ import annotations

######################################################################
class EmptyError(Exception):
    ''' class to represent an empty list exception '''
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message

######################################################################
class Node[T]:
    ''' class to represent a node in a doubly-linked list '''
    def __init__(self, data: T):
        self.data: T      = data
        self.prev: Node[T] = None  # pointer to the previous Node in the list
        self.next: Node[T] = None  # pointer to the next Node in the list

######################################################################
class LinkedList[T]:
    ''' class to implement a doubly-linked list '''
    __slots__ = ('_head', '_tail', '_size')

    def __init__(self) -> None:
        self._head: Node[T] = None   # head pointer: contains addy of one Node object
        self._tail: Node[T] = None   # tail pointer: contains addy of one Node object
        self._size: int     = 0      # number of entries in the list

    def __len__(self) -> int:
        ''' returns the number of entries in the linked list
        Returns:
            integer valued number of list entries
        '''
        return self._size

    def front(self) -> T:
        ''' method to return the data item at the front of the list without
            removing that node
        Returns:
            the T-valued item at the front of the list
        Raises:
            EmptyError if the list is empty
        '''
        if self._head is None:
            raise EmptyError('Linked List is empty')
        return self._head.data

    def back(self) -> T:
        ''' method to return the data item at the end of the list without
            removing that node
        Returns:
            the T-valued item at the end of the list
        Raises:
            EmptyError if the list is empty
        '''
        if self._tail is None:
            raise EmptyError('Linked List is empty')
        return self._tail.data

    def appendLeft(self, item: T) -> None:
        ''' adds the given T-type data item as part of a new Node to the left
            of the linked list
        Parameters:
            item: a type T data item to be included as the data in the inserted Node
        Raises:
            TypeError if non-empty list and item type does not match list entry types
        '''
        if self._head is not None and not isinstance(item, type(self._head.data)):
            raise TypeError('Cannot append a different datatype to what is already in the list')
        
        new_node = Node(item)
        if self._head is None:
            self._head = new_node
            self._tail = new_node
        else:
            new_node.next = self._head
            self._head.prev = new_node
            self._head = new_node
        self._size += 1

    def appendRight(self, item: T) -> None:
        ''' adds the given T-type data item as part of a new Node to the right 
            of the linked list
        Parameters:
            item: a type T data item to be included as the data in the inserted Node
        Raises:
            TypeError if non-empty list and item type does not match list entry types
        '''
        if self._head is not None and not isinstance(item, type(self._head.data)):
            raise TypeError('Cannot append a different datatype to what is already in the list')
        
        new_node = Node(item)
        if self._head is None:
            self._head = new_node
            self._tail = new_node
        else:
            self._tail.next = new_node
            new_node.prev = self._tail
            self._tail = new_node
        self._size += 1

    def popLeft(self) -> T:
        ''' removes the first Node in the linked list, returning the data item
            inside that Node
        Returns:
            a T type data item extracted from the removed Node
        Raises:
            EmptyError exception if list is empty
        '''
        if self._head == None:
            raise EmptyError("Can't pop from an empty list")
        
        pop_data = self._head.data
        self._head = self._head.next
        if self._head is not None:
            self._head.prev = None
        else:
            self._tail = None
            
        self._size -= 1
        return pop_data
            
    def popRight(self) -> T:
        ''' removes the last Node in the linked list, returning the data item
            inside that Node
        Returns:
            a T type data item extracted from the removed Node
        Raises:
            EmptyError exception if list is empty
        '''
        if self._tail is None:
            raise EmptyError("Can't pop from an empty list")
        
        pop_data = self._tail.data
        self._tail = self._tail.prev
        
        if self._tail is not None:
            self._tail.next = None
        else:
            self._head = None

        self._size -= 1
        return pop_data

    def __str__(self):
        ''' a str representation of the linked list data
        Returns:
            str representation of the linked list, showing head and tail
            pointers and list data items
        '''
        str_ = "head->"
        # start out at the head Node, and walk through Node by Node until we
        # reach the end of the linked list (i.e., the ._next entry is None)
        ptr_ = self._head
        while ptr_ is not None:
            str_ += "[" + repr(ptr_.data) + "]<->"   # use of repr will print quotes with strings
            ptr_ = ptr_.next  # move ptr_ to the next Node in the linked list

        if self._head != None: str_ = str_[:-3]  # remove the last "<->"
        str_ += "<-tail"
        return str_
        
###################
def main() -> None:
    # create a LinkedList and try out some various appends and pops
    print("Creating an empty linked list:")
    ll = LinkedList()
    print(ll)
    print(f"len(ll) = {len(ll)}")
    print()

    print("appending 12 to the right:")
    ll.appendRight(12)
    print(ll)
    print(f"len(ll) = {len(ll)}")
    print()

    print("appending 24 to the right:")
    ll.appendRight(24)
    print(ll)
    print(f"len(ll) = {len(ll)}")
    print()

    print("appending 36 to the right:")
    ll.appendRight(36)
    print(ll)
    print(f"len(ll) = {len(ll)}")
    print()

    print("popping from the left all three values in order:")
    for i in range(3):
        value = ll.popLeft()
        print(f"popped {value}")
        print(ll)
        print(f"len(ll) = {len(ll)}")
        print()

    print("attempting to popLeft from an empty list")
    try:
        value = ll.popLeft()
    except EmptyError as error:
        print(f"Correctly raised EmptyError: {error}")

    print('\nTesting appendLeft')
    ll.appendLeft(3)
    ll.appendLeft(21)
    ll.appendLeft(98)
    print(f'  Actual: {ll}')
    print(f'Expected: head->[98]->[21]->[3]<-tail')
    print(f'  Length: {len(ll)}')
    print(f'Expected: 3')

    print('\nTesting popRight')
    value = ll.popRight()
    print(f'  Popped: {value}')
    print(f'Expected: 3')
    print(f'  Actual: {ll}')
    print(f'Expected: head->[98]->[21]<-tail')
    print(f'  Length: {len(ll)}')
    print(f'Expected: 2')

    value = ll.popRight()
    print(f'  Popped: {value}')
    print(f'Expected: 21')
    print(f'  Actual: {ll}')
    print(f'Expected: head->[98]<-tail')
    print(f'  Length: {len(ll)}')
    print(f'Expected: 1')

    value = ll.popRight()
    print(f'  Popped: {value}')
    print(f'Expected: 98')
    print(f'  Actual: {ll}')
    print(f'Expected: head-><-tail')
    print(f'  Length: {len(ll)}')
    print(f'Expected: 0')

    print('\nTesting popRight on empty list (should raise error)')
    try:
        ll.popRight()
    except EmptyError as error:
        print(f'Correctly raised EmptyError: {error}')

    print('\nTesting appendLeft and popLeft mixed')
    ll.appendLeft(11)
    ll.appendLeft(22)
    ll.appendLeft(33)
    print(f'  Actual: {ll}')
    print(f'Expected: head->[33]->[22]->[11]<-tail')
    print(f'  Length: {len(ll)}')
    print(f'Expected: 3')

    value = ll.popLeft()
    print(f'Popped left: {value}')
    print(f'   Expected: 33')
    value = ll.popLeft()
    print(f'Popped left: {value}')
    print(f'   Expected: 22')
    value = ll.popLeft()
    print(f'Popped left: {value}')
    print(f'   Expected: 11')
    print(f'  Actual: {ll}')
    print(f'Expected: head-><-tail')
    print(f'  Length: {len(ll)}')
    print(f'Expected: 0')

    print('\nTesting mixed appendLeft and appendRight')
    ll.appendLeft(5)
    ll.appendRight(10)
    ll.appendLeft(2)
    ll.appendRight(15)
    print(f'  Actual: {ll}')
    print(f'Expected: head->[2]->[5]->[10]->[15]<-tail')
    print(f'  Length: {len(ll)}')
    print(f'Expected: 4')

    print("\nTesting front()")
    ll.appendRight(10)
    print(f"Front element: {ll.front()}")
    print(f"     Expected: 10")

    ll.appendRight(20)
    print(f"Front element: {ll.front()}")
    print(f"     Expected: 10")

    ll.appendLeft(5)
    print(f"  Front element after appendLeft(5): {ll.front()}")
    print(f"                           Expected: 5")

    print("\nTesting back()")
    print(f"Back element: {ll.back()}")
    print(f"    Expected: 20")

    ll.appendRight(30)
    print(f"  Back element after appendRight(30): {ll.back()}")
    print(f"                            Expected: 30")

    print("\nTesting front() and back() on an empty list (should raise error)")
    ll = LinkedList()

    print("Attempting front() on an empty list")
    try:
        value = ll.front()
    except EmptyError as error:
        print(f"Correctly raised EmptyError: {error}")

    print("Attempting back() on an empty list")
    try:
        value = ll.back()
    except EmptyError as error:
        print(f"Correctly raised EmptyError: {error}")

if __name__ == "__main__":
    main()