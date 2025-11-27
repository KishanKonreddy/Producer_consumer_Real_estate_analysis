# Assignment 1 – Producer–Consumer Concurrency Challenge

This project implements a classic Producer–Consumer pattern in Python using threads, a custom bounded blocking queue, and proper synchronization using `threading.Condition`. The implementation demonstrates thread coordination, blocking behavior, and inter-thread communication through wait/notify mechanisms.

---

## Overview

The solution includes:

- A **BoundedBlockingQueue** with:
  - Mutual exclusion
  - Blocking `put()` and `get()`
  - FIFO ordering
  - Clean shutdown via `close()`
- A **Producer** thread that reads items from a source container and inserts them into the queue.
- A **Consumer** thread that reads items from the queue and stores them in a destination container.
- Comprehensive **unit tests** validating queue behavior and multithreaded coordination.

The project is structured using clean, modular best practices.

---

## Project Structure

assignment_1/
├── src/
│ ├── queue.py # BoundedBlockingQueue implementation
│ ├── producer.py # Producer thread
│ ├── consumer.py # Consumer thread
│ └── main.py # Example entry point
├── tests/
│ └── test_producer_consumer.py
└── README.md



## Implementation Summary

### BoundedBlockingQueue
A custom blocking queue that:
- Blocks producers when full
- Blocks consumers when empty
- Uses `Condition` for synchronization
- Supports graceful shutdown with `close()`

### Producer
- Inherits from `Thread`
- Reads items from a source list
- Calls `put()` on the queue
- Closes the queue after finishing production

### Consumer
- Inherits from `Thread`
- Continuously calls `get()` on the queue
- Appends items into a destination list
- Stops when queue is closed and empty

### Unit Tests
The test suite validates:
- FIFO ordering
- Blocking behavior
- Close semantics
- Single and multiple consumer interactions
- End-to-end data transfer correctness

---

## Running the Program

From the project root:

python3 -m src.main



## Running Tests

Run all tests:

python3 -m unittest discover -s tests

Run a specific test:

python3 -m unittest tests.test_producer_consumer



## Author

Kishan Kumar Reddy Konreddy
Producer–Consumer Pattern
