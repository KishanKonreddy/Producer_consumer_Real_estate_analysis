"""
Consumer thread implementation.
"""

from __future__ import annotations
import logging
from threading import Thread
from typing import List, TypeVar

from .queue import BoundedBlockingQueue, QueueClosedError

T = TypeVar("T")

logging.basicConfig(level=logging.INFO)


class Consumer(Thread):
    """
    Consumer thread.

    Reads items from the shared BoundedBlockingQueue
    and stores them in a destination container.
    """

    def __init__(self, queue: BoundedBlockingQueue[T], destination: List[T], name: str | None = None) -> None:
        super().__init__(name=name or "Consumer")
        self.queue = queue
        self.destination = destination

    def run(self) -> None:
        logging.info(f"{self.name} started.")
        while True:
            try:
                item = self.queue.get()
            except QueueClosedError:
                logging.info(f"{self.name} exiting. Queue closed.")
                break

            self.destination.append(item)
        logging.info(f"{self.name} finished.")
