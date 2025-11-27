# Real Estate Sales Analysis (Connecticut, 2001–2023) – Functional & Stream-Based Python

This project is a small, production-style analytics tool built in Python to demonstrate:

- Functional programming
- Stream operations
- Data aggregation
- Lambda expressions

It analyzes the **Real Estate Sales 2001–2023** dataset published by the State of Connecticut and turns raw property transfer records into market insights (e.g., yearly trends, top towns, residential type comparison, price-to-assessment ratios, outlier towns, quarterly trends, etc.).

---

## 1. Problem Statement

The Connecticut Real Estate Sales dataset contains more than a million rows of property transactions recorded by towns across the state. In its raw CSV form, the data is not directly useful for decision-making. Stakeholders typically want to answer questions like:

- How has the **real estate market changed over time**?
- Which **towns** generate the highest total sales and the highest average prices?
- How do different **residential property types** compare (Single Family vs Condo, etc.)?
- Which towns tend to sell **far above their assessed values**?
- What is the **distribution of prices** by property type?
- Which towns have unusually **high numbers of outlier transactions**?

The goal of this project is to build a **Python command-line application** that:

1. **Reads** the CSV file using the standard library (no pandas or NumPy).
2. Uses **functional-style transformations** (map/filter/reduce patterns, lambdas, pure functions).
3. Performs **aggregation and grouping** across multiple dimensions (year, town, property type, residential type, quarter).
4. Prints the **results of all analyses to the console** in a clear, labeled format.

---

## 2. Dataset Choice & How It Fits the Assignment

The assignment requires:

> "Select or construct a CSV dataset that you feel best fits the problem and document your choices and assumptions as part of your solution."

### 2.1 Dataset Selected

I **selected** the official **Real Estate Sales 2001–2023** dataset from the Connecticut Open Data Portal and saved it as:
```
data/Real_Estate_Sales_2001-2023_GL.csv
```

**Dataset Source:** [Connecticut Real Estate Sales 2001-2018 - Data.gov](https://catalog.data.gov/dataset/real-estate-sales-2001-2018/resource/f7cb94d8-283c-476f-a966-cc8c9e1308b4)

Each row in this dataset represents a **recorded property sale**, with relevant fields including:

- **Town** – municipality where the property is located.
- **Date Recorded** – date the transaction was recorded.
- **Sale Amount** – transaction price in USD.
- **Property Type** – high-level category (Residential, Commercial, Industrial, Vacant Land, Apartments, etc.).
- **Residential Type** – more specific residential subtype (Single Family, Condo, Two Family, Three Family, Four Family, etc.).
- **Assessed Value** – value used by the local tax assessor.

### 2.2 Why this dataset best fits the problem

This dataset is a good fit for the assignment for several reasons:

- **Right shape for streams & functional programming**  
  The data is at **individual transaction level**, not pre-aggregated. That means:
  - We can **iterate** over a large number of rows from the CSV as plain Python dicts.
  - We can apply **functional-style operations** (map, filter, reduce-like patterns) on raw records.
  - We must implement **real aggregations**: group by year, town, property type, residential type, and quarter.

- **Natural for the required analyses**  
  The assignment focuses on "performing data analysis on sales data." This dataset supports:
  - Year-by-year and quarter-by-quarter market trends.
  - Town-level comparisons by total sales and by average price.
  - Residential property type comparisons (median vs average price).
  - Price-to-assessed-value ratios as a proxy for "market heat."
  - Price distribution and outlier detection by town and property type.

- **Realistic and reproducible**  
  The dataset is public, official, and well documented:
  - Anyone can download the same CSV and reproduce the analysis.
  - The heterogeneity (different property types, wide price range, occasional data issues) is realistic and not artificially simplified.

### 2.3 Assumptions documented in the solution

To keep the analysis consistent and realistic, I make the following **explicit assumptions**, which are implemented in the code:

1. **What counts as a "valid" sale?**  
   For core KPIs (totals, averages, distributions, etc.), a transaction is considered **valid** if:
   - **Sale Amount** is present and parsed successfully.
   - **Sale Amount** > 0.
   - **Sale Amount** ≤ 10,000,000 (extreme outliers above this are treated as data errors).
   - **Date Recorded** is a valid date and the year is between 2001 and 2024 (inclusive).

   These checks are performed in `loader.py` when constructing the in-memory list of records.

2. **How assessed values are used**  
   - Price-to-assessed-value ratio is only computed when **Assessed Value** > 0.
   - Town-level ratio statistics are computed only for towns with at least a minimum number of valid records (parameter `min_count`, typically 200 for the full dataset, smaller in unit tests).

3. **Handling missing or empty categories**  
   - Missing **Property Type** or **Residential Type** values are treated as empty strings and may be grouped under that empty category.
   - For residential type analysis, only records with **Property Type** == "Residential" are considered.

4. **Date parsing and derived fields**  
   **Date Recorded** is parsed using the known format (month/day/year).

   For each valid record the following derived fields are created:
   - **year** – integer year of the transaction.
   - **quarter** – integer quarter (1–4) derived from the month.
   - **year_quarter** – string key such as "2021-Q3".

5. **Outlier definition**  
   Outliers for `outlier_towns` are detected using the Interquartile Range (IQR) method:
   - Q1 = 25th percentile, Q3 = 75th percentile.
   - IQR = Q3 – Q1.
   - Any sale price < Q1 – 1.5 * IQR or > Q3 + 1.5 * IQR is considered an outlier.

These assumptions are both **implemented in the code** and **documented here**, directly satisfying the assignment requirement to document dataset choices and assumptions.

---

## 3. Project Structure
```
ASSIGNMENT - 2/
├── src/
│   ├── __init__.py
│   ├── loader.py                      # CSV parsing and cleaning into record dictionaries
│   ├── functional_queries.py          # Pure functional aggregations and analytics
│   ├── stream_utils.py                # Lazy stream helpers (map/filter-style generators)
│   └── main.py                        # Command-line interface that runs all analyses
├── tests/
│   ├── __init__.py
│   └── test_real_estate_small_unit.py # Small unit tests over handcrafted records
├── Dataset_Choices_and_Assumptions.docx # Separate written documentation
├── data/
│   └── Real_Estate_Sales_2001-2023_GL.csv # Connecticut real estate sales CSV
├── images/                            # Output screenshots
│   ├── Real_Estate_Analysis-1.png
│   ├── Real_Estate_Analysis-2.png
│
└── README.md
```

### 3.1 Core Modules Explained

#### `loader.py`
Handles CSV parsing and data cleaning:
- Reads the raw CSV file line by line
- Parses and validates each transaction record
- Filters out invalid sales (negative prices, extreme outliers)
- Creates derived fields (year, quarter, year_quarter)
- Returns a clean list of transaction dictionaries

#### `functional_queries.py`
Contains pure functional aggregation logic:
- All analysis functions (yearly trends, top towns, residential stats, etc.)
- Uses functional programming patterns (map, filter, reduce)
- Implements grouping, sorting, and statistical calculations
- Each function is pure (no side effects, same input → same output)

#### `stream_utils.py` - Lazy Stream Processing Library
This module provides a **functional stream processing library** that enables **lazy evaluation** and **memory-efficient data transformations**. Instead of processing all data at once (eager evaluation), streams process items one at a time, only when needed.

**Key Concepts:**
- **Lazy Evaluation**: Operations are not executed until the data is actually consumed (e.g., converted to a list or iterated over)
- **Memory Efficiency**: For large datasets (like 1M+ rows), streams avoid loading everything into memory
- **Composability**: Multiple stream operations can be chained together in a functional pipeline

**Available Stream Operations:**

1. **`stream(data)`** - Stream Creation
   - Converts any iterable (list, tuple, etc.) into a generator stream
   - Enables lazy evaluation on existing collections
   - Example: `stream([1, 2, 3, 4, 5])`

2. **`stream_filter(predicate, data)`** - Lazy Filtering
   - Filters items based on a predicate function
   - Only evaluates when items are consumed
   - Example: `stream_filter(lambda x: x['price'] > 100000, transactions)`

3. **`stream_map(func, data)`** - Lazy Transformation
   - Transforms each item using a function
   - Applies transformation one item at a time
   - Example: `stream_map(lambda x: x['sale_amount'] * 1.1, sales)`

4. **`stream_take(n, data)`** - Limit Operation
   - Takes only the first n items from the stream
   - Useful for getting top-N results or sampling
   - Example: `stream_take(10, sorted_towns)` (get top 10)

5. **`stream_skip(n, data)`** - Skip Operation
   - Skips the first n items in the stream
   - Useful for pagination or removing headers
   - Example: `stream_skip(5, transactions)` (skip first 5)

6. **`stream_distinct(data, key=None)`** - Deduplication
   - Removes duplicate items from the stream
   - Optional key function for custom comparison
   - Example: `stream_distinct(towns, key=lambda x: x['name'])`

7. **`stream_peek(action, data)`** - Non-Consuming Inspection
   - Performs an action on each item without consuming the stream
   - Useful for debugging or logging
   - Items pass through unchanged
   - Example: `stream_peek(lambda x: print(f"Processing: {x}"), data)`

**Example Usage in the Project:**
```python
# Filter valid transactions, map to sale amounts, then sum
total = sum(
    stream_map(
        lambda x: x['sale_amount'],
        stream_filter(
            lambda x: x['sale_amount'] > 0 and x['year'] == 2023,
            transactions
        )
    )
)

# Get top 10 towns by descending sales
top_towns = list(
    stream_take(
        10,
        stream(sorted(town_sales, key=lambda x: x['total'], reverse=True))
    )
)
```

**Benefits:**
- **Memory Efficient**: Processes millions of records without loading everything into memory
- **Composable**: Chain multiple operations together in a functional pipeline
- **Reusable**: Stream utilities work with any data type (dictionaries, objects, primitives)
- **Testable**: Pure functions make testing and debugging easier

#### `main.py`
Command-line interface that orchestrates the analysis:
- Loads data using `loader.py`
- Calls all analysis functions from `functional_queries.py`
- Formats and prints results to console in structured sections

---

## 4. How to Run the CLI Application

### 4.1 Prerequisites

- Python **3.8+** (uses standard library only, no external dependencies)
- Download the dataset from [Data.gov](https://catalog.data.gov/dataset/real-estate-sales-2001-2018/resource/f7cb94d8-283c-476f-a966-cc8c9e1308b4) and place it as `data/Real_Estate_Sales_2001-2023_GL.csv` in the `data/` folder.

---

### 4.2 Setup

From the project root (`ASSIGNMENT - 2`):
```bash
git clone <your-github-repo-url>.git
cd ASSIGNMENT-2

# Optional: Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

**Note:** This project uses only the Python standard library, so no `requirements.txt` or package installation is needed.

---

### 4.3 Run the CLI

The CLI entry point is `src/main.py`, exposed as a module.

From the project root:
```bash
python3 -m src.main
```

This will:

1. **Load and clean** the CSV into a list of Python dictionaries.
2. **Run all analysis functions** defined in `functional_queries.py`.
3. **Print the results** in clearly labeled sections, one per analytical question:
   - yearly market summary,
   - top towns by sales,
   - residential type statistics,
   - price-to-assessment ratios,
   - total market value,
   - yearly totals via functional pipeline,
   - top towns by average price,
   - price distributions by property type,
   - outlier towns,
   - quarterly trend with moving average.

---

## 5. How to Run the Tests

All core aggregation logic is covered by unit tests under the `tests/` directory using a small handcrafted sample of real-estate-like records.

From the project root:

### 5.1 Run all tests with discovery
```bash
python3 -m unittest discover -s tests -v
```

This will:

- Discover all test modules in the `tests/` directory.
- Run them in verbose mode (`-v`), showing each individual test name and status (e.g., "test_total_sales_all … ok").

---

### 5.2 What the Test Suite Covers

The test suite (`RealEstateSmallUnitTests`) verifies:

- **Correct behavior of:**
  - `total_sales_all`
  - `total_sales_year`
  - `yearly_sales_summary`
  - `top_towns_by_total_sales`
  - `residential_type_stats`
  - `price_to_assessed_ratio`
  - `quarterly_trend`

- **Edge cases such as:**
  - behavior on empty inputs (total sales = 0, no summary rows, etc.),
  - small samples still producing consistent ratios and trends,
  - correct ordering of towns and years in summaries.

These tests ensure that the functional building blocks behave as expected before they are applied to the full 1M+ row dataset.

---

## 6. Sample Outputs

![Real Estate Analysis 1](images/Real_Estate_Analysis-1.png)

![Real Estate Analysis 2](images/Real_Estate_Analysis-2.png)


The CLI prints each query in a clearly separated block. A typical excerpt looks like:
```
================================================================================
QUERY: Annual Sales Trends - Total Sales, Volume & Average Prices

QUESTION: How has the real estate market changed year by year?
WHAT WE CALCULATE: Group by year, compute transaction count, total sales, and average price.
TECHNIQUE: Sorting + groupby + map/lambda for aggregation

Last 10 Years:
2015: Transactions= 48,784 | Total Sales=$17,011,051,909 | Avg Price=$348,701
2016: Transactions= 47,363 | Total Sales=$14,865,850,491 | Avg Price=$313,871
...
```

Similar sections follow for:

- Top towns by total sales (2018–2023)
- Residential property type comparison
- Towns selling above assessed value
- Total market value (all years)
- Annual totals via filter → map → sum
- Top towns by average price (2021)
- Price distribution (percentiles) by property type (2022)
- Towns with highest outlier rates (2022)
- Quarterly price trends with moving average and Above/Below trend labels.

This combination of CLI output and unit tests demonstrates how functional programming techniques can be applied to a real, large-scale government dataset to produce clear, reusable analytics.

---

## 7. Data Source

**Dataset:** Real Estate Sales 2001-2018 (Connecticut)  
**Source:** [Data.gov - Connecticut Open Data Portal](https://catalog.data.gov/dataset/real-estate-sales-2001-2018/resource/f7cb94d8-283c-476f-a966-cc8c9e1308b4)  
**License:** Public Domain



## 9. Contributing

Contributions are welcome! Please feel free to submit a Pull Request.