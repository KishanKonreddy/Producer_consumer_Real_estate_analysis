import unittest
from typing import List

from src.queue import BoundedBlockingQueue, QueueClosedError
from src.producer import Producer
from src.consumer import Consumer


class TestBoundedBlockingQueue(unittest.TestCase):
    """Unit tests for the BoundedBlockingQueue class."""

    def test_put_and_get_single_item(self) -> None:
        queue: BoundedBlockingQueue[int] = BoundedBlockingQueue(capacity=2)

        queue.put(10)
        self.assertEqual(queue.size(), 1)

        item = queue.get()
        self.assertEqual(item, 10)
        self.assertEqual(queue.size(), 0)

    def test_fifo_order(self) -> None:
        """Queue should preserve FIFO ordering."""
        queue: BoundedBlockingQueue[int] = BoundedBlockingQueue(capacity=5)

        data = [1, 2, 3, 4]
        for value in data:
            queue.put(value)

        result = [queue.get() for _ in data]
        self.assertEqual(result, data)

    def test_close_empty_queue_raises_on_get(self) -> None:
        """Getting from a closed and empty queue should raise QueueClosedError."""
        queue: BoundedBlockingQueue[int] = BoundedBlockingQueue(capacity=1)
        queue.close()

        with self.assertRaises(QueueClosedError):
            _ = queue.get()

    def test_cannot_put_after_close(self) -> None:
        """Putting into a closed queue should raise RuntimeError."""
        queue: BoundedBlockingQueue[int] = BoundedBlockingQueue(capacity=1)
        queue.close()

        with self.assertRaises(RuntimeError):
            queue.put(1)


class TestProducerConsumerIntegration(unittest.TestCase):
    """Integration tests for Producer and Consumer using the queue."""

    def test_all_items_transferred_single_consumer(self) -> None:
        """All items from source must appear in destination in same order."""
        source: List[int] = list(range(20))
        destination: List[int] = []

        queue: BoundedBlockingQueue[int] = BoundedBlockingQueue(capacity=3)

        producer = Producer(source=source, queue=queue)
        consumer = Consumer(queue=queue, destination=destination)

        producer.start()
        consumer.start()

        producer.join(timeout=5)
        consumer.join(timeout=5)

        # Both threads should be finished
        self.assertFalse(producer.is_alive(), "Producer thread did not finish.")
        self.assertFalse(consumer.is_alive(), "Consumer thread did not finish.")

        # Destination should have exactly the source data in order
        self.assertEqual(destination, source)

    def test_multiple_consumers_share_work(self) -> None:
        """
        When using multiple consumers, all items from source should still be
        consumed exactly once in total.
        """
        source: List[int] = list(range(50))
        dest1: List[int] = []
        dest2: List[int] = []

        queue: BoundedBlockingQueue[int] = BoundedBlockingQueue(capacity=5)

        producer = Producer(source=source, queue=queue)
        consumer1 = Consumer(queue=queue, destination=dest1)
        consumer2 = Consumer(queue=queue, destination=dest2)

        producer.start()
        consumer1.start()
        consumer2.start()

        producer.join(timeout=5)
        consumer1.join(timeout=5)
        consumer2.join(timeout=5)

        self.assertFalse(producer.is_alive(), "Producer thread did not finish.")
        self.assertFalse(consumer1.is_alive(), "Consumer-1 thread did not finish.")
        self.assertFalse(consumer2.is_alive(), "Consumer-2 thread did not finish.")

        # Combine results and check that all items are present exactly once
        combined = sorted(dest1 + dest2)
        self.assertEqual(combined, source)


if __name__ == "__main__":
    unittest.main()
