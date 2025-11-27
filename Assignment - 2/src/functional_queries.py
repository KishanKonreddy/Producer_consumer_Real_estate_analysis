"""
Functional-stream operations for real estate data analysis.
Demonstrates functional programming concepts: map, filter, reduce, lambda, generators.
"""

from functools import reduce
from itertools import groupby
from operator import itemgetter
from typing import List, Dict, Any, Iterator


# ------------------- QUERY 1 -------------------
def yearly_sales_summary(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    QUERY 1: Annual Sales Trends - Total Sales, Transaction Volume & Average Prices
    
    QUESTION: How has the real estate market changed year by year?
    
    WHAT WE CALCULATE:
        - Group records by year
        - Compute count, total sales, and average price per year
        
    TECHNIQUE:
        - Sorting + groupby for aggregation
        - Lambda with map for extracting sale amounts
        - Sum and len for aggregations
        
    Returns:
        List of dicts with year, count, total_sales, avg_price
    """
    # Sort before groupby (required for itertools.groupby)
    sorted_records = sorted(records, key=itemgetter("year"))

    result = []

    for year, group in groupby(sorted_records, key=itemgetter("year")):
        group_list = list(group)
        total = sum(map(lambda r: r["sale_amount"], group_list))
        count = len(group_list)
        avg = total / count if count > 0 else 0

        result.append({
            "year": year,
            "count": count,
            "total_sales": total,
            "avg_price": avg
        })

    return result


# ------------------- QUERY 2 -------------------
def top_towns_by_total_sales(records: List[Dict[str, Any]], start_year: int = 2018) -> List[Dict[str, Any]]:
    """
    QUERY 2: Top Performing Towns - Highest Total Sales Volume
    
    QUESTION: Since 2018, which towns have the highest total sales?
    
    WHAT WE CALCULATE:
        - Filter years >= start_year
        - Group by town
        - Compute total sales per town
        - Return top 10 towns
        
    TECHNIQUE:
        - Filter with lambda for year filtering
        - Groupby for town aggregation
        - Sorted with lambda for ranking
        
    Args:
        records: List of record dictionaries
        start_year: Filter records from this year onwards
        
    Returns:
        Top 10 towns by total sales value
    """
    filtered = list(filter(lambda r: r["year"] >= start_year, records))
    sorted_recs = sorted(filtered, key=itemgetter("town"))

    result = []

    for town, group in groupby(sorted_recs, key=itemgetter("town")):
        group_list = list(group)
        total = sum(map(lambda r: r["sale_amount"], group_list))
        result.append({"town": town, "total_sales": total})

    return sorted(result, key=lambda x: x["total_sales"], reverse=True)[:10]


# ------------------- QUERY 3 -------------------
def residential_type_stats(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    QUERY 3: Residential Property Type Comparison - Median vs Average Prices
    
    QUESTION: How do different residential property types differ in price?
    
    WHAT WE CALCULATE:
        - Filter to residential properties only
        - Group by residential_type
        - Compute count, median, and average price
        
    TECHNIQUE:
        - Filter with lambda
        - Map to extract prices
        - Sorted for median calculation
        
    Returns:
        Statistics per residential type, sorted by median price
    """
    residential = list(filter(lambda r: r["property_type"] == "Residential", records))
    sorted_recs = sorted(residential, key=itemgetter("residential_type"))

    result = []

    for rtype, group in groupby(sorted_recs, key=itemgetter("residential_type")):
        prices = list(map(lambda r: r["sale_amount"], group))
        prices_sorted = sorted(prices)
        count = len(prices)
        median = prices_sorted[count // 2] if count else 0
        avg = sum(prices) / count if count else 0

        result.append({
            "type": rtype,
            "count": count,
            "median": median,
            "avg": avg
        })

    return sorted(result, key=lambda x: x["median"], reverse=True)


# ------------------- QUERY 4 -------------------
def price_to_assessed_ratio(records: List[Dict[str, Any]], min_count: int = 200) -> List[Dict[str, Any]]:
    """
    QUERY 4: Market Value Assessment - Sale Price to Assessed Value Ratio
    
    QUESTION: Which towns sell most above their tax assessment?
    
    WHAT WE CALCULATE:
        - Ratio = sale_amount / assessed_value for each record
        - Group by town
        - Compute average ratio per town
        - Filter towns with sufficient data (min_count)
        
    TECHNIQUE:
        - Filter to remove invalid assessed values
        - List comprehension for ratio calculation
        - Groupby for town aggregation
        
    Args:
        records: List of record dictionaries
        min_count: Minimum transactions required per town
        
    Returns:
        Top 10 towns by average price-to-assessed ratio
    """
    valid = list(filter(lambda r: r["assessed_value"] > 0, records))
    sorted_recs = sorted(valid, key=itemgetter("town"))

    result = []

    for town, group in groupby(sorted_recs, key=itemgetter("town")):
        group_list = list(group)
        if len(group_list) < min_count:
            continue

        ratios = [r["sale_amount"] / r["assessed_value"] for r in group_list]
        avg_ratio = sum(ratios) / len(ratios)
        result.append({"town": town, "avg_ratio": avg_ratio, "count": len(group_list)})

    return sorted(result, key=lambda x: x["avg_ratio"], reverse=True)[:10]


# ------------------- QUERY 5 -------------------
def total_sales_all(records: List[Dict[str, Any]]) -> float:
    """
    QUERY 5: Total Market Value - Cumulative Sales Using Reduce
    
    QUESTION: What is the total dollar value of all real estate transactions?
    
    WHAT WE CALCULATE:
        - Sum of all sale amounts across entire dataset
        
    TECHNIQUE:
        - Pure functional reduce with lambda
        - Accumulator pattern
        
    Returns:
        Total sales value as float
    """
    return reduce(lambda acc, r: acc + r["sale_amount"], records, 0.0)


# ------------------- QUERY 6 -------------------
def total_sales_year(records: List[Dict[str, Any]], year: int) -> float:
    """
    QUERY 6: Annual Total Sales - Filter-Map-Sum Pipeline
    
    QUESTION: What was the total sales value for a specific year?
    
    WHAT WE CALCULATE:
        - Filter records for specified year
        - Sum all sale amounts
        
    TECHNIQUE:
        - Filter with lambda
        - Map to extract amounts
        - Terminal sum operation
        
    Args:
        records: List of record dictionaries
        year: Target year to analyze
        
    Returns:
        Total sales for specified year
    """
    filtered = filter(lambda r: r["year"] == year, records)
    return sum(map(lambda r: r["sale_amount"], filtered))


# ------------------- QUERY 7 -------------------
def top_towns_by_average_price(records: List[Dict[str, Any]], year: int, min_count: int = 50) -> List[Dict[str, Any]]:
    """
    QUERY 7: Top Towns by Average Price - Pure Functional Grouping
    
    QUESTION: Which towns have the highest average sale prices in a given year?
    
    WHAT WE CALCULATE:
        - Filter to specific year
        - Group by town
        - Compute average price per town
        - Require minimum transaction count
        
    TECHNIQUE:
        - Filter with generator
        - Groupby with attrgetter
        - Lambda for sorting
        
    Args:
        records: List of record dictionaries
        year: Target year
        min_count: Minimum transactions per town
        
    Returns:
        Top 10 towns by average price
    """
    filtered = list(filter(lambda r: r["year"] == year, records))
    sorted_recs = sorted(filtered, key=itemgetter("town"))

    result = []

    for town, group in groupby(sorted_recs, key=itemgetter("town")):
        group_list = list(group)
        if len(group_list) < min_count:
            continue

        avg = sum(map(lambda r: r["sale_amount"], group_list)) / len(group_list)
        result.append({"town": town, "avg_price": avg, "count": len(group_list)})

    return sorted(result, key=lambda x: x["avg_price"], reverse=True)[:10]


# ------------------- QUERY 8 -------------------
def price_distribution(records: List[Dict[str, Any]], year: int) -> List[Dict[str, Any]]:
    """
    QUERY 8: Price Distribution Analysis - Statistical Percentiles
    
    QUESTION: What is the price distribution across different property types?
    
    WHAT WE CALCULATE:
        - Filter to specific year
        - Group by property_type
        - Calculate 25th, 50th (median), and 75th percentiles
        
    TECHNIQUE:
        - Filter with lambda
        - Map to extract prices
        - Sorted for percentile calculation
        - Index-based percentile extraction
        
    Args:
        records: List of record dictionaries
        year: Target year
        
    Returns:
        Percentile statistics per property type
    """
    filtered = list(filter(lambda r: r["year"] == year, records))
    sorted_recs = sorted(filtered, key=itemgetter("property_type"))

    result = []

    for ptype, group in groupby(sorted_recs, key=itemgetter("property_type")):
        prices = sorted(map(lambda r: r["sale_amount"], group))
        n = len(prices)
        if n < 10: 
            continue

        p25 = prices[int(n * 0.25)]
        p50 = prices[int(n * 0.50)]
        p75 = prices[int(n * 0.75)]

        result.append({
            "property_type": ptype,
            "count": n,
            "p25": p25,
            "median": p50,
            "p75": p75,
            "iqr": p75 - p25 #Inter Quartile range
        })

    return sorted(result, key=lambda x: x["median"], reverse=True)


# ------------------- QUERY 9 -------------------
def outlier_towns(records: List[Dict[str, Any]], year: int) -> List[Dict[str, Any]]:
    """
    QUERY 9: Anomaly Detection - Statistical Outliers Using IQR Method
    
    QUESTION: Which towns have the most price outliers (unusual transactions)?
    
    WHAT WE CALCULATE:
        - Filter to specific year
        - Group by town
        - Calculate IQR (Interquartile Range)
        - Identify outliers: values < Q1-1.5*IQR or > Q3+1.5*IQR
        - Compute outlier rate percentage
        
    TECHNIQUE:
        - Statistical outlier detection
        - Filter with lambda for outlier counting
        - Percentage calculations
        
    Args:
        records: List of record dictionaries
        year: Target year
        
    Returns:
        Top 10 towns by outlier rate
    """
    filtered = list(filter(lambda r: r["year"] == year, records))
    sorted_recs = sorted(filtered, key=itemgetter("town"))

    result = []

    for town, group in groupby(sorted_recs, key=itemgetter("town")):
        prices = sorted(map(lambda r: r["sale_amount"], group))
        n = len(prices)
        if n < 30:
            continue

        q1 = prices[int(n * 0.25)]
        q3 = prices[int(n * 0.75)]
        iqr = q3 - q1
        lb = q1 - 1.5 * iqr
        ub = q3 + 1.5 * iqr

        outliers = len(list(filter(lambda p: p < lb or p > ub, prices)))
        rate = outliers / n * 100

        result.append({"town": town, "outlier_rate": rate, "outliers": outliers, "count": n})

    return sorted(result, key=lambda x: x["outlier_rate"], reverse=True)[:10]


# ------------------- QUERY 10 -------------------
def quarterly_trend(records: List[Dict[str, Any]], window: int = 4) -> List[Dict[str, Any]]:
    """
    QUERY 10: Time-Series Trend Analysis - Quarterly Moving Averages
    
    QUESTION: How do average prices change over time by quarter, and what is the smoothed trend?
    
    WHAT WE CALCULATE:
        - Group by year_quarter (e.g., '2021-Q3')
        - Compute average sale price per quarter
        - Calculate 4-quarter (1-year) moving average
        - Label each quarter as Above/Below trend
        
    TECHNIQUE:
        - Groupby for quarterly aggregation
        - Windowing for moving average calculation
        - Conditional logic for trend detection
        
    Args:
        records: List of record dictionaries
        window: Size of moving average window (default 4 quarters)
        
    Returns:
        Last 10 quarters with trend analysis
    """
    # Sort by year_quarter (already like '2019-Q1', '2019-Q2', ...)
    sorted_recs = sorted(records, key=itemgetter("year_quarter"))

    # 1. Aggregate avg price per quarter
    quarters = []
    for yq, group in groupby(sorted_recs, key=itemgetter("year_quarter")):
        group_list = list(group)
        prices = [r["sale_amount"] for r in group_list]
        avg_price = sum(prices) / len(prices)
        quarters.append({"year_quarter": yq, "avg_price": avg_price, "count": len(prices)})

    # 2. Compute moving average and trend
    for i in range(len(quarters)):
        if i < window - 1:
            quarters[i]["moving_avg"] = None
            quarters[i]["trend"] = "No Data"
        else:
            window_values = [q["avg_price"] for q in quarters[i - window + 1:i + 1]]
            ma = sum(window_values) / window
            quarters[i]["moving_avg"] = ma
            quarters[i]["trend"] = "Above Trend" if quarters[i]["avg_price"] > ma else "Below Trend"

    # Return last 10 quarters for display
    return quarters[-10:]