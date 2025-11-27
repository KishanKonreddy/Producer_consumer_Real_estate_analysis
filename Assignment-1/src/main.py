"""
Example demonstrating Producer → Queue → Consumer data transfer.
"""

from .producer import Producer
from .consumer import Consumer
from .queue import BoundedBlockingQueue


def main() -> None:
    source_data = list(range(10))
    dest_data = []

    queue = BoundedBlockingQueue[int](capacity=3)

    producer = Producer(source=source_data, queue=queue)
    consumer = Consumer(queue=queue, destination=dest_data)

    producer.start()
    consumer.start()

    producer.join()
    consumer.join()

    print("Source:     ", source_data)
    print("Destination:", dest_data)


if __name__ == "__main__":
    main()
