"""
Stack and Queue implementations.

Stack -> LIFO (Last In, First Out): like a pile of plates.
Queue -> FIFO (First In, First Out): like a line at a bank.
"""
from collections import deque


class Stack:
    """A LIFO stack built on a Python list (the top is the END of the list)."""

    def __init__(self):
        self._items = []

    def push(self, item):
        """Add an item to the top. O(1) amortized."""
        self._items.append(item)

    def pop(self):
        """Remove and return the top item. O(1)."""
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        """Return the top item without removing it. O(1)."""
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)

    def __len__(self):
        return len(self._items)

    def __repr__(self):
        return "Stack({})".format(self._items)


class Queue:
    """
    A FIFO queue built on collections.deque.

    Why not a list? list.pop(0) shifts every other item left, so it is O(n).
    deque.popleft() is O(1).
    """

    def __init__(self):
        self._items = deque()

    def enqueue(self, item):
        """Add an item to the back. O(1)."""
        self._items.append(item)

    def dequeue(self):
        """Remove and return the front item. O(1)."""
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self._items.popleft()

    def peek(self):
        """Return the front item without removing it. O(1)."""
        if self.is_empty():
            raise IndexError("peek from empty queue")
        return self._items[0]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)

    def __len__(self):
        return len(self._items)

    def __repr__(self):
        return "Queue({})".format(list(self._items))
