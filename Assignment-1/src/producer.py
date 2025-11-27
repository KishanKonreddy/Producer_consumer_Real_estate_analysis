"""
Producer thread implementation.
"""

from __future__ import annotations
import logging
from threading import Thread
from typing import List, TypeVar

from .queue import BoundedBlockingQueue

T = TypeVar("T")

logging.basicConfig(level=logging.INFO)


class Producer(Thread):
    """
    Producer thread.

    Reads items from a source container and puts them into the
    shared BoundedBlockingQueue.
    """

    def __init__(self, source: List[T], queue: BoundedBlockingQueue[T], name: str | None = None) -> None:
        super().__init__(name=name or "Producer")
        self.source = source
        self.queue = queue

    def run(self) -> None:
        logging.info("Producer started.")
        for item in self.source:
            self.queue.put(item)
        logging.info("Producer finished. Closing queue.")
        self.queue.close()
