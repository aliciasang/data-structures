class EmptyError(Exception):
    ''' class extending Exception to better document stack errors '''
    def __init__(self, message: str):
        self.message = message

#####################################################################

class Stack[T]:
    ''' class to implement a stack ADT using a Python list '''

    __slots__ = ("_data")  # a Python list

    def __init__(self) -> None:
        self._data = []

    def __len__(self) -> int:
        ''' allows the len function to be called using a Stack object, e.g.,
               stack = Stack()
               print(len(stack))
        Returns:
            number of elements in the stack, as an integer
        '''
        return len(self._data)

    def push(self, item: T) -> None: 
        ''' pushes a given item of arbitrary type onto the stack
        Parameters:
            item: an item of arbitrary type
        Returns:
            None
        Raises:
            TypeError if trying to push an item of different type onto
                a stack already containing that type
        '''
        if len(self._data) > 0 and not isinstance(item, type(self._data[0])):
            msg = f"cannot push type {type(item).__name__} " + \
                  f"onto stack containing type {type(self._data[0]).__name__}"
            raise TypeError(msg)

        # if correct type, put at the top of the stack by appending to the list
        self._data.append(item)  # calling Python list .append()

    def pop(self) -> T:
        ''' removes the topmost element from the stack and returns that element
        Returns:
            the topmost item, of arbitrary type
        Raises:
            EmptyError exception if the stack is empty
        '''
        if len(self._data) == 0:
            raise EmptyError('Error in Stack.pop(): stack is empty')
        return self._data.pop()  # calling Python list .pop()

    def top(self) -> T:
        ''' returns the topmost element from the stack without modifying the stack
        Returns:
            the topmost item, of arbitrary type
        Raises:
            EmptyError exception if the stack is empty
        '''
        if len(self._data) == 0:
            raise EmptyError('Error in Stack.top(): stack is empty')
        return self._data[-1]

    def isEmpty(self) -> bool:
        ''' indicates whether the stack is empty
        Returns:
            True if the stack is empty, False otherwise
        '''
        return len(self._data) == 0

    def __str__(self) -> str:
        ''' creates a string representation of the data in the stack, using
            the maximum str length of any one datum as a centering guide 
        Returns:
            a string representation of the stack
        '''
        result = "--- top ---\n"
        if len(self._data) > 0:
            max_len    = max(len(str(datum)) for datum in self._data)
            half_width = max(0, (len(result) - max_len) // 2)
            # "\n".join creates a new string, deliminted by "\n" characters, where
            # the elements between each "\n" in the string are drawn from the
            # reverse of the data list so as to print the stack from top to bottom
            result += "\n".join(f"{datum:>{max_len + half_width}}" for datum in self._data[::-1])
            result += "\n--- bot ---"
        else:
            result += "--- bot ---"
            
        return result

#####################################################################
    
def main() -> None:
    s = Stack()
    print("Current stack is:")
    print(s)
    print('*' * 40)


    for item in [1,2,3,4]:
        print(f"pushing {item} onto stack...")
        s.push(item)
        print("Current stack is:")
        print(s)
        print('*' * 40)

    try:
        print("trying to push 'five' onto the stack...")
        s.push("five")
    except TypeError as err:
        print(f"Correctly caught TypeError exception: {err}")

    print("Current stack is:")
    print(s)
    print('*' * 40)

    fou = s.pop()
    print(f"Popping topmost element: {fou}")

    print("Current stack is:")
    print(s)
    print('*' * 40)

    print("Emptying stack...")
    while len(s) > 0:
        print(f"\t Popping topmost element: {s.pop()}")
        print("\t Current stack is:")
        print('\t' + str(s).replace('\n', '\n\t'))
        print()
    print('*' * 40)

    try:
        print("trying to pop from empty stack...")
        none = s.pop()
    except EmptyError as err:
        print(f"Correctly caught EmtpyError exception: {err}")


if __name__ == "__main__":
    main()