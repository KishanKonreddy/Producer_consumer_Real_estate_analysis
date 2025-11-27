"""
Thread-safe bounded blocking queue implementation using Condition
for mutual exclusion and wait/notify synchronization.
"""

from __future__ import annotations
from threading import Condition
from typing import Generic, List, TypeVar

T = TypeVar("T")


class QueueClosedError(Exception):
    """Raised when attempting to get from a closed and empty queue."""
    pass


class BoundedBlockingQueue(Generic[T]):
    """
    A thread-safe bounded blocking queue.

    - put(item) blocks when queue is full.
    - get() blocks when queue is empty.
    - close() wakes waiting threads and prevents further puts.
    """

    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")

        self._capacity = capacity
        self._buffer: List[T] = []
        self._closed = False
        self._condition = Condition()

    def put(self, item: T) -> None:
        """Put an item into the queue. Blocks if the queue is full."""
        with self._condition:
            if self._closed:
                raise RuntimeError("Cannot put into a closed queue.")

            while len(self._buffer) >= self._capacity:
                self._condition.wait()

            self._buffer.append(item)
            self._condition.notify_all()

    def get(self) -> T:
        """Get an item from the queue. Blocks if empty until closed."""
        with self._condition:
            while not self._buffer and not self._closed:
                self._condition.wait()

            if not self._buffer and self._closed:
                raise QueueClosedError("Queue is closed and empty.")

            item = self._buffer.pop(0)
            self._condition.notify_all()
            return item

    def close(self) -> None:
        """Close the queue and wake all waiting threads."""
        with self._condition:
            self._closed = True
            self._condition.notify_all()

    def size(self) -> int:
        """Return current number of items in the queue."""
        with self._condition:
            return len(self._buffer)

    @property
    def closed(self) -> bool:
        """Check whether queue has been closed."""
        with self._condition:
            return self._closed
