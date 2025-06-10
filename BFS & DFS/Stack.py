from __future__ import annotations
from EmptyError import EmptyError
from LinkedList import LinkedList
from typing import TypeVar, Generic

T = TypeVar('T')

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._list = LinkedList[T]()

    def __len__(self) -> int:
        return self._list.__len__()
    
    def isEmpty(self) -> bool:
        return len(self._list) == 0
    
    def push(self, item: T) -> None:
        self._list.appendRight(item)

    def pop(self) -> T:
        if self.isEmpty():
            raise EmptyError("Cannot pop from an empty stack")
        return self._list.popRight()

    def top(self) -> T:
        if self.isEmpty():
            raise EmptyError("Cannot peek at an empty stack")
        return self._list.top()
    
    def __str__(self):
        return str(self._list)
    
def main():
    stack = Stack[int]()

if __name__ == "__main__":
    main()