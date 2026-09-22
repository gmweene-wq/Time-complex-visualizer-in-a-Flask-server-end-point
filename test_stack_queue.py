"""
Test suite for Stack, Queue and the algorithms that use them.

Run with:   python -m unittest -v test_stack_queue.py
(or:        pytest -v test_stack_queue.py)
"""
import unittest

from data_structures import Stack, Queue
from stack_queue_algorithms import (
    is_balanced, reverse_items, TwoStackQueue, hot_potato,
    STACK_QUEUE_ALGORITHMS,
)


class TestStack(unittest.TestCase):

    def setUp(self):
        self.stack = Stack()

    # --- empty stack ---
    def test_new_stack_is_empty(self):
        self.assertTrue(self.stack.is_empty())
        self.assertEqual(self.stack.size(), 0)
        self.assertEqual(len(self.stack), 0)

    def test_pop_empty_raises(self):
        with self.assertRaises(IndexError):
            self.stack.pop()

    def test_peek_empty_raises(self):
        with self.assertRaises(IndexError):
            self.stack.peek()

    # --- basic behaviour ---
    def test_push_increases_size(self):
        self.stack.push(1)
        self.stack.push(2)
        self.assertEqual(self.stack.size(), 2)
        self.assertFalse(self.stack.is_empty())

    def test_pop_returns_last_pushed(self):
        self.stack.push('a')
        self.stack.push('b')
        self.assertEqual(self.stack.pop(), 'b')

    def test_lifo_order(self):
        for i in range(5):
            self.stack.push(i)
        popped = [self.stack.pop() for _ in range(5)]
        self.assertEqual(popped, [4, 3, 2, 1, 0])

    def test_peek_does_not_remove(self):
        self.stack.push(10)
        self.assertEqual(self.stack.peek(), 10)
        self.assertEqual(self.stack.size(), 1)

    def test_pop_until_empty_then_raises(self):
        self.stack.push(1)
        self.stack.pop()
        self.assertTrue(self.stack.is_empty())
        with self.assertRaises(IndexError):
            self.stack.pop()

    # --- edge cases ---
    def test_accepts_none_and_mixed_types(self):
        self.stack.push(None)
        self.stack.push("x")
        self.stack.push([1, 2])
        self.assertEqual(self.stack.pop(), [1, 2])
        self.assertEqual(self.stack.pop(), "x")
        self.assertIsNone(self.stack.pop())

    def test_interleaved_push_pop(self):
        self.stack.push(1)
        self.stack.push(2)
        self.assertEqual(self.stack.pop(), 2)
        self.stack.push(3)
        self.assertEqual(self.stack.pop(), 3)
        self.assertEqual(self.stack.pop(), 1)

    def test_large_number_of_items(self):
        for i in range(100_000):
            self.stack.push(i)
        self.assertEqual(self.stack.size(), 100_000)
        self.assertEqual(self.stack.peek(), 99_999)

    def test_repr(self):
        self.stack.push(1)
        self.assertEqual(repr(self.stack), "Stack([1])")


class TestQueue(unittest.TestCase):

    def setUp(self):
        self.queue = Queue()

    # --- empty queue ---
    def test_new_queue_is_empty(self):
        self.assertTrue(self.queue.is_empty())
        self.assertEqual(self.queue.size(), 0)
        self.assertEqual(len(self.queue), 0)

    def test_dequeue_empty_raises(self):
        with self.assertRaises(IndexError):
            self.queue.dequeue()

    def test_peek_empty_raises(self):
        with self.assertRaises(IndexError):
            self.queue.peek()

    # --- basic behaviour ---
    def test_enqueue_increases_size(self):
        self.queue.enqueue(1)
        self.queue.enqueue(2)
        self.assertEqual(self.queue.size(), 2)
        self.assertFalse(self.queue.is_empty())

    def test_dequeue_returns_first_enqueued(self):
        self.queue.enqueue('a')
        self.queue.enqueue('b')
        self.assertEqual(self.queue.dequeue(), 'a')

    def test_fifo_order(self):
        for i in range(5):
            self.queue.enqueue(i)
        out = [self.queue.dequeue() for _ in range(5)]
        self.assertEqual(out, [0, 1, 2, 3, 4])

    def test_peek_does_not_remove(self):
        self.queue.enqueue(10)
        self.queue.enqueue(20)
        self.assertEqual(self.queue.peek(), 10)
        self.assertEqual(self.queue.size(), 2)

    def test_dequeue_until_empty_then_raises(self):
        self.queue.enqueue(1)
        self.queue.dequeue()
        self.assertTrue(self.queue.is_empty())
        with self.assertRaises(IndexError):
            self.queue.dequeue()

    # --- edge cases ---
    def test_accepts_none_and_mixed_types(self):
        self.queue.enqueue(None)
        self.queue.enqueue("x")
        self.assertIsNone(self.queue.dequeue())
        self.assertEqual(self.queue.dequeue(), "x")

    def test_interleaved_enqueue_dequeue(self):
        self.queue.enqueue(1)
        self.queue.enqueue(2)
        self.assertEqual(self.queue.dequeue(), 1)
        self.queue.enqueue(3)
        self.assertEqual(self.queue.dequeue(), 2)
        self.assertEqual(self.queue.dequeue(), 3)

    def test_large_number_of_items(self):
        for i in range(100_000):
            self.queue.enqueue(i)
        self.assertEqual(self.queue.size(), 100_000)
        self.assertEqual(self.queue.peek(), 0)

    def test_repr(self):
        self.queue.enqueue(1)
        self.assertEqual(repr(self.queue), "Queue([1])")


class TestIsBalanced(unittest.TestCase):

    def test_balanced_cases(self):
        for text in ["", "()", "([]{})", "{[()()]}", "a(b)c[d]"]:
            with self.subTest(text=text):
                self.assertTrue(is_balanced(text))

    def test_unbalanced_cases(self):
        for text in ["(", ")", "(]", "([)]", "(()", "())", "}{"]:
            with self.subTest(text=text):
                self.assertFalse(is_balanced(text))


class TestReverseItems(unittest.TestCase):

    def test_reverse_list(self):
        self.assertEqual(reverse_items([1, 2, 3]), [3, 2, 1])

    def test_reverse_string(self):
        self.assertEqual("".join(reverse_items("hello")), "olleh")

    def test_reverse_empty(self):
        self.assertEqual(reverse_items([]), [])


class TestTwoStackQueue(unittest.TestCase):

    def test_fifo_order(self):
        q = TwoStackQueue()
        for i in range(5):
            q.enqueue(i)
        self.assertEqual([q.dequeue() for _ in range(5)], [0, 1, 2, 3, 4])

    def test_interleaved_operations(self):
        q = TwoStackQueue()
        q.enqueue(1)
        q.enqueue(2)
        self.assertEqual(q.dequeue(), 1)
        q.enqueue(3)                      # goes to inbox while outbox has 2
        self.assertEqual(q.dequeue(), 2)
        self.assertEqual(q.dequeue(), 3)
        self.assertTrue(q.is_empty())

    def test_empty_raises(self):
        with self.assertRaises(IndexError):
            TwoStackQueue().dequeue()

    def test_len(self):
        q = TwoStackQueue()
        q.enqueue(1)
        q.enqueue(2)
        q.dequeue()
        self.assertEqual(len(q), 1)


class TestHotPotato(unittest.TestCase):

    def test_classic_example(self):
        names = ["Bill", "David", "Susan", "Jane", "Kent", "Brad"]
        self.assertEqual(hot_potato(names, 7), "Susan")

    def test_single_person_wins(self):
        self.assertEqual(hot_potato(["Dida"], 3), "Dida")

    def test_zero_passes_last_person_wins(self):
        self.assertEqual(hot_potato([1, 2, 3], 0), 3)

    def test_empty_raises(self):
        with self.assertRaises(ValueError):
            hot_potato([], 3)


class TestVisualiserWrappers(unittest.TestCase):
    """Every wrapper must run for n = 0 and small n without crashing."""

    def test_all_wrappers_run(self):
        for name, func in STACK_QUEUE_ALGORITHMS.items():
            for n in [0, 1, 7, 100]:
                with self.subTest(algorithm=name, n=n):
                    func(n)

    def test_names_are_safe_filenames(self):
        for name, func in STACK_QUEUE_ALGORITHMS.items():
            self.assertEqual(func.__name__, name)


if __name__ == '__main__':
    unittest.main(verbosity=2)
