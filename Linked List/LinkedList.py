from __future__ import annotations

# https://docs.python.org/3/tutorial/errors.html#user-defined-exceptions
# Want to define our own custom Exception class...
class EmptyError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message

class Node[T]:
    ''' class to implement a single node object in a singly-linked
        linked list '''
    __slots__ = ('data', 'next')

    def __init__(self, data: T):
        self.data: T       = data
        self.next: Node[T] = None  # can point to another Node object

class LinkedList[T]:
    ''' class to implement a singly-linked linked list '''

    def __init__(self) -> None:
        self._head: Node[T] = None   # head pointer: variable w/ addy of Node object
        self._tail: Node[T] = None   # tail pointer: variable w/ addy of Node object
        self._size: int     = 0

    def __len__(self) -> int:
        return self._size

    def appendLeft(self, item: T) -> None:
        ''' append the given T-type data item as part of a new Node to the left
            side of the linked list
        Parameters:
            item: a type T data item to be included as the data in the inserted Node
        Returns:
            nothing
        '''
        new_node = Node(item)
        new_node.next = self._head
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
        # remember to reset the tail pointer, and, when appropriate, 
        # the head pointer
        
        new_node = Node(item)  # construct a new node object
        
        if self._size == 0:
            # appending to an empty list
            self._head = new_node
            self._tail = new_node  # or self._tail = self._head
        else:
            # appending to a non-empty list
            self._tail.next = new_node
            self._tail      = new_node

        self._size += 1

    def popLeft(self) -> T:
        ''' removes the first Node in the linked list, returning the data item
            inside that Node
        Returns:
            a T type data item extracted from the removed Node
        Raises:
            EmptyError exception if list is empty
        '''
        # remember to handle the special case of an empty list (what should the
        # head and tail pointers be in that case?) and remember to update the
        # head & tail pointer(s) when appropriate
        if self._size == 0:
            raise EmptyError("Cannot popLeft from an empty list")

        value = self._head.data

        if self._head == self._tail:
            # list of size one when popping, so set both _head and _tail to None
            self._head = self._tail = None
        else:
            # list size > 1, so advance head to next in list
            self._head = self._head.next

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
        # Remember to handle the special case of an empty list (what should the
        # head and tail pointers be in that case?)
        # 
        # Note: This one is trickier because you always have to walk (almost)
        # all the way through the list in order to know what the new tail
        # should be.
        #
        # Remember to update the head & tail pointer(s) when appropriate.
        if self._size == 0:
            raise EmptyError("Cannot popRight from an empty list")

        value = self._tail.data

        if self._head == self._tail:
            # list of size one when popping, so set both _head and _tail to None
            self._head = self._tail = None
        else:
            # list size > 1, so advance head to next in list
            current_node = self._head
            while current_node.next != self._tail:
                current_node = current_node.next

            current_node.next = None
            self._tail = current_node
        
        self._size -= 1
        return value

    def __str__(self):
        ''' returns a str representation of the linked list data
        Returns:
            an str representation of the linked list, showing head pointer
                and data tiems
        '''
        result = "head->"

        # start out at the head Node, and walk through Node by Node until we
        # reach the end of the linked list (i.e., the ._next entry is None)
        ptr = self._head   # temp variable initially w/ same addy as _head
        while ptr is not None:
            result += f"[{str(ptr.data)}]->"    # [55]->
            ptr = ptr.next    # advancing ptr to the next node in the list
        if self._size > 0:
            result = result[:-2]  # dump the last -> when non-empty
        result += "<-tail"
        return result

        
def main():
    # create a LinkedList and try out some various appends and pops
    print("Creating an empty linked list:")
    ll = LinkedList()
    print(ll)
    print(f"len(ll) = {len(ll)}")
    print()

    print("appending 55 to the right:")
    ll.appendRight(55)
    print(ll)
    print(f"len(ll) = {len(ll)}")
    print()

    print("appending 66 to the right:")
    ll.appendRight(66)
    print(ll)
    print(f"len(ll) = {len(ll)}")
    print()

    print("appending 77 to the right:")
    ll.appendRight(77)
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
    ll.appendLeft(1)
    ll.appendLeft(45)
    ll.appendLeft(632)
    print(f'  Actual: {ll}')
    print(f'Expected: head->[632]->[45]->[1]<-tail')
    print(f'  Length: {len(ll)}')
    print(f'Expected: 3')

    print('\nTesting popRight')
    value = ll.popRight()
    print(f'  Popped: {value}')
    print(f'Expected: 1')
    print(f'  Actual: {ll}')
    print(f'Expected: head->[632]->[45]<-tail')
    print(f'  Length: {len(ll)}')
    print(f'Expected: 2')

    value = ll.popRight()
    print(f'  Popped: {value}')
    print(f'Expected: 45')
    print(f'  Actual: {ll}')
    print(f'Expected: head->[632]<-tail')
    print(f'  Length: {len(ll)}')
    print(f'Expected: 1')

    value = ll.popRight()
    print(f'  Popped: {value}')
    print(f'Expected: 632)')
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
    ll.appendLeft(100)
    ll.appendLeft(200)
    ll.appendLeft(300)
    print(f'  Actual: {ll}')
    print(f'Expected: head->[300]->[200]->[100]<-tail')
    print(f'  Length: {len(ll)}')
    print(f'Expected: 3')

    value = ll.popLeft()
    print(f'Popped left: {value}')
    print(f'   Expected: 300')
    value = ll.popLeft()
    print(f'Popped left: {value}')
    print(f'   Expected: 200')
    value = ll.popLeft()
    print(f'Popped left: {value}')
    print(f'   Expected: 100')
    print(f'  Actual: {ll}')
    print(f'Expected: head-><-tail')
    print(f'  Length: {len(ll)}')
    print(f'Expected: 0')

    print('\nTesting mixed appendLeft and appendRight')
    ll.appendLeft(1)
    ll.appendRight(2)
    ll.appendLeft(0)
    ll.appendRight(3)
    print(f'  Actual: {ll}')
    print(f'Expected: head->[0]->[1]->[2]->[3]<-tail')
    print(f'  Length: {len(ll)}')
    print(f'Expected: 4')

if __name__ == "__main__":
    main()