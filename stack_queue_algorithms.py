"""
Algorithms that use Stacks and Queues.

Part 1: the real algorithms (take real data, used by the tests).
Part 2: visualiser wrappers (take a size n, build the input, run the algorithm).
        These plug into the Algorithms dictionary in app.py.
"""
from data_structures import Stack, Queue


# ---------------------------------------------------------------
# Part 1: real algorithms
# ---------------------------------------------------------------

BRACKET_PAIRS = {')': '(', ']': '[', '}': '{'}


def is_balanced(text):
    """Check if brackets are balanced, e.g. '([]{})' -> True. Stack, O(n)."""
    stack = Stack()
    for ch in text:
        if ch in '([{':
            stack.push(ch)
        elif ch in BRACKET_PAIRS:
            if stack.is_empty() or stack.pop() != BRACKET_PAIRS[ch]:
                return False
    return stack.is_empty()


def reverse_items(items):
    """Reverse a sequence by pushing everything then popping. Stack, O(n)."""
    stack = Stack()
    for item in items:
        stack.push(item)
    result = []
    while not stack.is_empty():
        result.append(stack.pop())
    return result


class TwoStackQueue:
    """
    A queue made from two stacks.
    Each item is moved from inbox to outbox at most once,
    so each operation is O(1) *amortized*.
    """

    def __init__(self):
        self._inbox = Stack()
        self._outbox = Stack()

    def enqueue(self, item):
        self._inbox.push(item)

    def dequeue(self):
        if self._outbox.is_empty():
            while not self._inbox.is_empty():
                self._outbox.push(self._inbox.pop())
        if self._outbox.is_empty():
            raise IndexError("dequeue from empty queue")
        return self._outbox.pop()

    def is_empty(self):
        return self._inbox.is_empty() and self._outbox.is_empty()

    def __len__(self):
        return len(self._inbox) + len(self._outbox)


def hot_potato(people, passes):
    """
    Pass the potato `passes` times; whoever holds it is out.
    Repeat until one person is left. Queue, O(n * passes).
    """
    if not people:
        raise ValueError("need at least one person")
    queue = Queue()
    for person in people:
        queue.enqueue(person)
    while queue.size() > 1:
        for _ in range(passes):
            queue.enqueue(queue.dequeue())
        queue.dequeue()
    return queue.dequeue()


# ---------------------------------------------------------------
# Part 2: visualiser wrappers (each takes only n)
# ---------------------------------------------------------------

def stack_push_pop(n):
    """Push n items, then pop them all. Expected: O(n)."""
    stack = Stack()
    for i in range(n):
        stack.push(i)
    while not stack.is_empty():
        stack.pop()


def queue_enqueue_dequeue(n):
    """Enqueue n items, then dequeue them all. Expected: O(n)."""
    queue = Queue()
    for i in range(n):
        queue.enqueue(i)
    while not queue.is_empty():
        queue.dequeue()


def list_as_queue(n):
    """The WRONG way: a list with pop(0). Expected: O(n^2)."""
    items = list(range(n))
    while items:
        items.pop(0)


def balanced_brackets(n):
    """Check a balanced string of length ~n. Expected: O(n)."""
    third = n // 6
    text = '(' * third + '[' * third + '{' * third + '}' * third + ']' * third + ')' * third
    is_balanced(text)


def reverse_with_stack(n):
    """Reverse a list of n items. Expected: O(n)."""
    reverse_items(range(n))


def two_stack_queue(n):
    """Enqueue n, then dequeue n using two stacks. Expected: O(n) total."""
    queue = TwoStackQueue()
    for i in range(n):
        queue.enqueue(i)
    while not queue.is_empty():
        queue.dequeue()


def hot_potato_game(n):
    """Hot potato with n people, 7 passes. Expected: O(n) (passes is fixed)."""
    if n == 0:
        return
    hot_potato(list(range(n)), 7)


STACK_QUEUE_ALGORITHMS = {
    'stack_push_pop': stack_push_pop,
    'queue_enqueue_dequeue': queue_enqueue_dequeue,
    'list_as_queue': list_as_queue,
    'balanced_brackets': balanced_brackets,
    'reverse_with_stack': reverse_with_stack,
    'two_stack_queue': two_stack_queue,
    'hot_potato_game': hot_potato_game,
}
