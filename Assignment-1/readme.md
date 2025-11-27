# Assignment 1 – Producer–Consumer Concurrency Challenge

This project implements a classic **Producer–Consumer pattern** in Python using threads, a custom bounded blocking queue, and proper synchronization using `threading.Condition`. The implementation demonstrates thread coordination, blocking behavior, and inter-thread communication through wait/notify mechanisms.

---

## 1. Overview

The solution includes:

* A **BoundedBlockingQueue** with:
   * Mutual exclusion
   * Blocking `put()` and `get()`
   * FIFO ordering
   * Clean shutdown via `close()`
* A **Producer thread** that reads items from a source container and inserts them into the queue.
* A **Consumer thread** that reads items from the queue and stores them in a destination container.
* **Comprehensive unit tests** validating queue behavior and multithreaded coordination.


---

## 2. Project Structure
```
ASSIGNMENT-1/
├── src/
│   ├── __init__.py
│   ├── queue.py           # BoundedBlockingQueue implementation
│   ├── producer.py        # Producer thread
│   ├── consumer.py        # Consumer thread
│   └── main.py            # Example entry point
├── tests/
│   ├── __init__.py
│   └── test_producer_consumer.py  # Unit tests
└── README.md
```

---

## 3. Implementation Summary

### 3.1 BoundedBlockingQueue

A custom thread-safe blocking queue that:

* **Blocks producers** when the queue is full
* **Blocks consumers** when the queue is empty
* Uses **`threading.Condition`** for efficient synchronization
* Supports **graceful shutdown** with `close()` method
* Maintains **FIFO (First-In-First-Out)** ordering
* Provides **thread-safe** `put()` and `get()` operations

**Key Features:**
- Bounded capacity to prevent memory overflow
- Wait/notify mechanism for thread coordination
- Proper handling of closed state
- Exception handling for closed queue operations

### 3.2 Producer

* Inherits from `threading.Thread`
* Reads items from a source list/container
* Calls `put()` on the queue to insert items
* **Closes the queue** after finishing production
* Handles queue full conditions gracefully

**Responsibilities:**
- Generate or fetch data items
- Insert items into the bounded queue
- Signal completion to consumers

### 3.3 Consumer

* Inherits from `threading.Thread`
* Continuously calls `get()` on the queue
* Appends items into a destination list/container
* **Stops automatically** when queue is closed and empty
* Handles queue empty conditions gracefully

**Responsibilities:**
- Retrieve items from the queue
- Process or store retrieved items
- Terminate when no more items are available

---

## 4. How to Run the Program

### 4.1 Prerequisites

- Python **3.8+** (uses standard library only)
- No external dependencies required

---

### 4.2 Setup

From the project root (`ASSIGNMENT-1`):
```bash
cd ASSIGNMENT-1

# Optional: Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

**Note:** This project uses only the Python standard library, so no package installation is needed.

---

### 4.3 Run the Program

From the project root:
```bash
python3 -m src.main
```

This will:

1. Create a bounded blocking queue with specified capacity
2. Start one or more producer threads
3. Start one or more consumer threads
4. Demonstrate thread-safe data transfer
5. Print logs showing producer/consumer activities
6. Gracefully shut down all threads

---

## 5. How to Run the Tests

The test suite validates all aspects of the producer-consumer implementation.

From the project root:

### 5.1 Run all tests with discovery
```bash
python3 -m unittest discover -s tests -v
```

This will:

- Discover all test modules in the `tests/` directory
- Run them in verbose mode (`-v`), showing each individual test name and status

---

### 5.2 Run a specific test module
```bash
python3 -m unittest tests.test_producer_consumer -v
```

---

### 5.3 What the Test Suite Covers

The test suite validates:

**Queue Behavior:**
- **FIFO ordering** - items are retrieved in the order they were inserted
- **Blocking behavior** - `put()` blocks when full, `get()` blocks when empty
- **Capacity enforcement** - queue respects maximum size limit
- **Thread safety** - concurrent operations don't cause race conditions

**Shutdown Semantics:**
- **Close behavior** - queue properly closes and signals consumers
- **Graceful termination** - consumers stop when queue is closed and empty
- **Exception handling** - operations on closed queue raise appropriate exceptions

**Multi-threaded Coordination:**
- **Single producer, single consumer** - basic data transfer works correctly
- **Multiple consumers** - multiple threads can safely consume from the same queue
- **End-to-end correctness** - all produced items are consumed exactly once
- **No data loss** - all items transferred successfully without duplication

**Edge Cases:**
- Empty queue behavior
- Full queue behavior
- Concurrent put/get operations
- Close during active production/consumption

---

## 6. Sample Output
```
[Producer-1] Starting production...
[Producer-1] Put item: 1
[Consumer-1] Got item: 1
[Producer-1] Put item: 2
[Producer-1] Put item: 3
[Consumer-1] Got item: 2
[Consumer-1] Got item: 3
[Producer-1] Finished. Closing queue.
[Consumer-1] Queue closed and empty. Exiting.

Summary:
- Items produced: 3
- Items consumed: 3
- Queue operations: Successful
```

---

## 7. Key Concepts Demonstrated

### Concurrency Patterns
- Classic producer-consumer problem solution
- Thread-safe data structure implementation
- Wait/notify synchronization mechanism

### Synchronization Primitives
- **`threading.Lock`** - mutual exclusion
- **`threading.Condition`** - wait/notify coordination
- **`threading.Thread`** - concurrent execution

### Design Principles
- Clean separation of concerns (queue, producer, consumer)
- Modular, testable code structure
- Graceful shutdown handling
- Comprehensive error handling

---

## 8. Technical Details

### Thread Coordination
- Producers wait when queue is full
- Consumers wait when queue is empty
- Condition variable notifies waiting threads when state changes

### Memory Safety
- Bounded queue prevents unbounded memory growth
- All operations are thread-safe with proper locking

### Termination
- Producer closes queue after completion
- Consumers detect closed state and terminate gracefully
- No orphaned threads or resource leaks