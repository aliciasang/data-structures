import ctypes


# for generic type T, see
# https://docs.python.org/3/whatsnew/3.12.html#pep-695-type-parameter-syntax
class List[T]:
    __slots__ = ('_array',              # reference to the ctypes array
                 '_num_user_items',     # current number of user's items in the List
                 '_capacity',           # total length of the ctypes array
                 '_num_resizes',        # number of array resizes performed
                 '_num_copies_append',  # number of item-to-item copies req'd on appending
                 '_num_copies_remove',  # number of item-to-item copies req'd on removing
                 '_growth_type',        # type of growth we are using to resize array
                 '_growth_value',       # additive or multiplier (depending on growth type)
                 '_type')               # type of objects in the list
            
    def __init__(self, growth_type = 'fixed', growth_value = 2):
        ''' initializer for a List class object, which allocates space for
            a length-1 initally empty underlying array 
            
            Args:
                growth_type: 'fixed' or 'relative' (default is 'fixed')
                growth_value: value to add or multiply by, depending on growth_type
            
            '''
        self._num_user_items = 0                                   # number of user items currently in the List
        self._capacity       = 1                                   # default List capacity at startup is 1
        self._array          = self._makeArray(self._capacity)     # creates an array with specified capacity
        self._growth_type    = growth_type                         # defines fixed or relative
        self._growth_value   = growth_value                        # value to add or multiply by

        # for internal stats (see comments above)
        self._num_resizes = 0
        self._num_copies_append = 0
        self._num_copies_remove = 0
        self._type = None

    def getInternalStats(self) -> dict:
        ''' method to return a dictionary containing information about the
            resizing-related statistics
        Returns:
            a dictionary with:
                current List capacity
                total number of resizes performed
                total number of item-to-item copies resulting from an append
                total number of item-to-item copies resulting from a remove
        '''
        return {"capacity"      : self._capacity, \
                "resizes"       : self._num_resizes, \
                "append_copies" : self._num_copies_append, \
                "remove_copies" : self._num_copies_remove}

    def _makeArray(self, capacity: int) -> ctypes.Array:
        ''' private method to reserve space for a low-level array of a
            given capacity
        Parameters:
            capacity: integer size of the array to be created
        Returns:
            a ctypes low-level array whose size is the given capacity
        '''
        ArrayType = (capacity * ctypes.py_object)  # py_object defined in ctypes
        return ArrayType() # create and return an array of py_object of size capacity

    def __len__(self) -> int:
        
        ''' returns number of user items currently stored in the List
        Returns:
            integer count of number of user items
        '''
        return self._num_user_items # already an int, don't need to convert to int again

    def __getitem__(self, index: int) -> T:
        ''' returns the item in the List at the given index
        Parameters:
            index: integer index between 0 and length - 1
        Returns:
            item of type T at the given index
        Raises:
            IndexError exception if index is invalid (i.e., negative or
                >= the number of user items in the List)
        '''
        if index < 0 or index >= self._num_user_items:
            raise IndexError('Index is invalid: Index must not be negative or greater than the capacity of the array')
        return self._array[index]
    
    def __setitem__(self, index: int, new_item: T) -> None:
        ''' sets the item in the List at the given index to the new 
            type-T item provided
        Parameters:
            index:    integer index between 0 and length - 1
            new_item: type-T item (must match type of items already in list)
        Returns:
            self._array: contains new_item at given index
        Raises:
            IndexError exception if index is invalid (i.e., negative or
                >= the number of user items in the List)
            TypeError exception if type of item does not match types already
                present in the List (first appended item determines List type)
        '''

        if index < 0 or index >= self._num_user_items:
            raise IndexError('Index is invalid: Index must not be negative or greater than the capacity of the array')
        if self._num_user_items >0 and type(new_item) != type(self._array[0]):
            raise TypeError('Type of item does not match types already present in the list')
        self._array[index] = new_item

    def append(self, new_item: T) -> None:
        ''' appends the given item to the List
        Parameters:
            new_item: type-T item to append to the List
        Returns:
            Nothing
        Raises:
            TypeError exception if type of item does not match types already
                present in the List (first appended item determines List type)
        '''

        if self._type is None:
            self._type = type(new_item)
        elif type(new_item) != self._type:
            raise TypeError('Type of item does not match types already present in the list')

        if self._num_user_items == self._capacity: # check whether array is full, and if so, allocate more space
            if self._growth_type == 'fixed':
                new_capacity = self._capacity + self._growth_value
            elif self._growth_type == 'relative':
                new_capacity = int(self._capacity * self._growth_value)
                if new_capacity <= self._capacity:
                    new_capacity = self._capacity + 1
            else:
                raise ValueError('Unknown growth type')
            
            self._resizeArray(new_capacity)

        self._array[self._num_user_items] = new_item
        self._num_user_items += 1

    def _float_equivalent(self, a: float, b: float, relative: float = 1e-9) -> bool:
        return abs(a - b) <= relative * max(abs(a), abs(b), 1.0)

    def remove(self, item: T) -> None:
        ''' removes the first occurrence of item in the List
        Parameters:
            item: type-T element to remove from the List
        Returns:
            self, with first item removed
        Raises:
            ValueError exception if given item does not exist in the List
        '''
        found = False
        for i in range(self._num_user_items):
            if (isinstance(item, float) and isinstance(self._array[i], float) and self._float_equivalent(self._array[i], item)) or self._array[i] == item:
                found = True
                for j in range(i, self._num_user_items - 1):
                    self._array[j] = self._array[j + 1]
                    self._num_copies_remove += 1
                self._array[self._num_user_items - 1] = None
                self._num_user_items -= 1
                break
        if not found:
            raise ValueError('Given item does not exist in the List')

    def _resizeArray(self, new_capacity: int) -> None:
        ''' private method to resize the underlying array to a specific
            capacity, copying elements from the old array into a new larger array
            
            Args: 
                new_capacity: integer size of new array'''
        new_array = self._makeArray(new_capacity)
        for index in range(self._num_user_items):
            new_array[index] = self._array[index]

        self._array = new_array
        self._num_resizes += 1
        self._num_copies_append += self._num_user_items
        self._capacity = new_capacity

    def __str__(self) -> str:
        ''' a string representation of this List
        Returns:
            a printable string format of the List contents
        '''
        result = "["
        for i in range(self._num_user_items):
            result += repr(self._array[i]) + ","
        # remove any trailing comma (for non-empty lLsts only)
        if self._num_user_items != 0: result = result[:-1]
        result += "]"
        return result


def main() -> None:
    l_fixed = List(growth_type='fixed', growth_value=2)
    l_relative = List(growth_type='relative', growth_value=2)

    for i in range(10):
        l_fixed.append(i)
        l_relative.append(i)

    print("Fixed growth list:", l_fixed)
    print("Relative growth list:", l_relative)
    print("Fixed stats:", l_fixed.getInternalStats())
    print("Relative stats:", l_relative.getInternalStats())

if __name__ == "__main__":
    main()