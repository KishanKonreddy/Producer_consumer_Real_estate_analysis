# Intuit Assignment – Python Data Analysis & Concurrency

This repository contains two independent Python mini-projects:

1. **Producer–Consumer Concurrency Demo** – a classic multithreaded producer–consumer implementation using a bounded blocking queue.
2. **Real Estate Sales Analysis (Connecticut, 2001–2023)** – a functional, stream-based data analysis CLI.

Each project lives in its own folder and has its own `README.md` with full details on design, setup, and usage.

---

## Repository Structure
```
.
├── ASSIGNMENT-1/                  # Project 1: Producer–Consumer concurrency demo
│   ├── src/
│   ├── tests/
│   └── README.md
├── ASSIGNMENT-2/                  # Project 2: Real Estate Sales data analysis CLI
│   ├── src/
│   ├── tests/
│   ├── data/
│   ├── images/
│   └── README.md
└── README.md                      # This file
```

---

## Assignment - 1: Producer–Consumer Concurrency Demo

**Location:** `ASSIGNMENT-1/`

A multithreaded Python implementation demonstrating the classic **producer–consumer problem** using:
- Thread-safe bounded blocking queue
- Multiple producer and consumer threads
- Synchronization primitives (locks, conditions)
- Graceful shutdown mechanism

**Key Features:**
- Configurable number of producers and consumers
- Bounded queue with blocking put/get operations
- Thread-safe operations with proper synchronization
- Comprehensive unit tests
- Detailed logging of thread activities

---

## Assignment - 2: Real Estate Sales Analysis (Connecticut, 2001–2023)

**Location:** `ASSIGNMENT-2/`

A production-style analytics CLI tool built in Python demonstrating:
- Functional programming patterns
- Stream-based lazy evaluation
- Data aggregation and grouping
- Lambda expressions and pure functions

**Analyzes:**
- 1M+ property transactions from Connecticut (2001–2023)
- Yearly and quarterly market trends
- Top towns by total sales and average price
- Residential property type comparisons
- Price-to-assessment ratios
- Outlier detection and price distributions

**Dataset Source:** [Connecticut Real Estate Sales - Data.gov](https://catalog.data.gov/dataset/real-estate-sales-2001-2018/resource/f7cb94d8-283c-476f-a966-cc8c9e1308b4)

**Key Features:**
- Uses only Python standard library (no pandas/NumPy)
- Functional-style transformations (map/filter/reduce patterns)
- Lazy stream processing for memory efficiency
- Multi-dimensional aggregations (year, town, property type, quarter)
- Comprehensive unit test coverage

---

## Quick Start

### ASSIGNMENT-1: Producer–Consumer
```bash
cd ASSIGNMENT-1
python3 -m src.main
python3 -m unittest discover -s tests -v
```

### ASSIGNMENT-2: Real Estate Analysis
```bash
cd ASSIGNMENT-2
python3 -m src.main
python3 -m unittest discover -s tests -v
```

---

## Requirements

- **Python 3.8+**
- Both projects use only the Python standard library
- No external dependencies required

---

## Testing

Both projects include comprehensive unit test suites:
```bash
# Test ASSIGNMENT-1
cd ASSIGNMENT-1
python3 -m unittest discover -s tests -v

# Test ASSIGNMENT-2
cd ASSIGNMENT-2
python3 -m unittest discover -s tests -v
```
