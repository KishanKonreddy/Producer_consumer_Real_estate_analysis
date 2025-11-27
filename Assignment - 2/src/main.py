"""
Main entry point for Real Estate Sales Analysis.
Demonstrates functional programming without pandas using pure Python.
"""

from .loader import load_data
from .functional_queries import (
    yearly_sales_summary,
    top_towns_by_total_sales,
    residential_type_stats,
    price_to_assessed_ratio,
    total_sales_all,
    total_sales_year,
    top_towns_by_average_price,
    price_distribution,
    outlier_towns,
    quarterly_trend,
)


def print_header(title: str, question: str, what: str, technique: str):
    """Helper function to print formatted query headers."""
    print("\n" + "="*80)
    print(f"QUERY: {title}")
    print("="*80)
    print(f"QUESTION: {question}")
    print(f"WHAT WE CALCULATE: {what}")
    print(f"TECHNIQUE: {technique}")
    print("="*80)


def main():
    """Main execution function."""
    print("="*80)
    print("REAL ESTATE SALES ANALYSIS - FUNCTIONAL PROGRAMMING")
    print("Demonstrating: map, filter, reduce, lambda, generators, stream operations")
    print("="*80)
    
    print("\nLoading dataset...")
    records = load_data("data/Real_Estate_Sales_2001-2023_GL.csv")
    
    if not records:
        print("No data loaded. Exiting.")
        return

    # ==================== QUERY 1 ====================
    print_header(
        "Annual Sales Trends - Total Sales, Volume & Average Prices",
        "How has the real estate market changed year by year?",
        "Group by year, compute count, total sales, and average price",
        "Sorting + groupby + map/lambda for aggregation"
    )
    summary = yearly_sales_summary(records)
    print("\nLast 10 Years:")
    for row in summary[-10:]:
        print(f"  {row['year']}: "
              f"Transactions={row['count']:>6,} | "
              f"Total Sales=${row['total_sales']:>15,.0f} | "
              f"Avg Price=${row['avg_price']:>10,.0f}")

    # ==================== QUERY 2 ====================
    print_header(
        "Top Performing Towns - Highest Total Sales (2018-2023)",
        "Since 2018, which towns have the highest total sales volume?",
        "Filter by year >= 2018, group by town, sum sales, rank top 10",
        "Filter with lambda + groupby + sorted with lambda"
    )
    top_towns = top_towns_by_total_sales(records, start_year=2018)
    print("\nTop 10 Towns:")
    for i, town in enumerate(top_towns, 1):
        print(f"  {i:>2}. {town['town']:<30} ${town['total_sales']:>15,.0f}")

    # ==================== QUERY 3 ====================
    print_header(
        "Residential Property Type Comparison - Median vs Average",
        "How do different residential property types (Single Family, Condo, etc.) differ in price?",
        "Filter residential only, group by type, compute median and average",
        "Filter with lambda + map for prices + sorted for median"
    )
    res_stats = residential_type_stats(records)
    print("\nResidential Type Statistics:")
    print(f"  {'Type':<25} {'Count':>10} {'Median':>15} {'Average':>15}")
    print("  " + "-"*68)
    for row in res_stats:
        if row['type']:  # Skip empty types
            print(f"  {row['type']:<25} {row['count']:>10,} "
                  f"${row['median']:>13,.0f} ${row['avg']:>13,.0f}")

    # ==================== QUERY 4 ====================
    print_header(
        "Market Value Assessment - Price-to-Assessed Ratio by Town",
        "Which towns have sale prices that exceed tax assessments the most?",
        "Calculate ratio = sale_amount / assessed_value, group by town, average ratio",
        "Filter for valid assessments + list comprehension + groupby"
    )
    ratio_stats = price_to_assessed_ratio(records, min_count=200)
    print("\nTop 10 Towns (Sales Above Assessment):")
    print(f"  {'Rank':<6} {'Town':<30} {'Avg Ratio':>12} {'Count':>8}")
    print("  " + "-"*60)
    for i, row in enumerate(ratio_stats, 1):
        print(f"  {i:>2}.   {row['town']:<30} {row['avg_ratio']:>10.2f}x {row['count']:>8,}")

    # ==================== QUERY 5 ====================
    print_header(
        "Total Market Value - Cumulative Sales Using Reduce",
        "What is the total dollar value of all real estate transactions?",
        "Sum all sale amounts across entire dataset using reduce",
        "Pure functional reduce with lambda accumulator"
    )
    total = total_sales_all(records)
    print(f"\n  Total Real Estate Sales: ${total:,.2f}")
    print(f"  Dataset Coverage: {min(r['year'] for r in records)} - {max(r['year'] for r in records)}")

    # ==================== QUERY 6 ====================
    print_header(
        "Annual Total Sales - Filter-Map-Sum Pipeline",
        "What were the total sales values for recent years?",
        "Filter by year, map to amounts, sum",
        "Filter with lambda + map + terminal sum operation"
    )
    print("\nRecent Years:")
    for y in [2019, 2020, 2021, 2022]:
        total_y = total_sales_year(records, y)
        print(f"  Year {y}: ${total_y:>18,.0f}")

    # ==================== QUERY 7 ====================
    print_header(
        "Top Towns by Average Price - Pure Functional Grouping (2021)",
        "Which towns had the highest average sale prices in 2021?",
        "Filter to 2021, group by town, compute average (min 50 transactions)",
        "Filter + groupby + lambda sorting"
    )
    top_avg = top_towns_by_average_price(records, year=2021, min_count=50)
    print("\nTop 10 Towns by Average Price (2021):")
    print(f"  {'Rank':<6} {'Town':<30} {'Avg Price':>15} {'Count':>8}")
    print("  " + "-"*65)
    for i, row in enumerate(top_avg, 1):
        print(f"  {i:>2}.   {row['town']:<30} ${row['avg_price']:>13,.0f} {row['count']:>8,}")

    # ==================== QUERY 8 ====================
    print_header(
        "Price Distribution Analysis - Statistical Percentiles (2022)",
        "What is the price distribution across different property types?",
        "Group by property type, calculate Q1, median, Q3, IQR",
        "Filter + map + sorted for percentile calculation"
    )
    dist = price_distribution(records, year=2022)
    print("\n2022 Price Distributions by Property Type:")
    print(f"  {'Property Type':<25} {'Count':>8} {'P25':>12} {'Median':>12} {'P75':>12} {'IQR':>12}")
    print("  " + "-"*85)
    for row in dist[:5]:  # Top 5 by median
        if row['property_type']:
            print(f"  {row['property_type']:<25} {row['count']:>8,} "
                  f"${row['p25']:>10,.0f} ${row['median']:>10,.0f} "
                  f"${row['p75']:>10,.0f} ${row['iqr']:>10,.0f}")

    # ==================== QUERY 9 ====================
    print_header(
        "Anomaly Detection - Statistical Outliers Using IQR (2022)",
        "Which towns have the most unusual price transactions?",
        "Calculate IQR per town, identify outliers (< Q1-1.5*IQR or > Q3+1.5*IQR)",
        "Filter + groupby + statistical outlier detection with lambda"
    )
    outliers = outlier_towns(records, year=2022)
    print("\nTop 10 Towns by Outlier Rate (2022):")
    print(f"  {'Rank':<6} {'Town':<30} {'Outlier Rate':>13} {'Outliers':>10} {'Total':>8}")
    print("  " + "-"*72)
    for i, row in enumerate(outliers, 1):
        print(f"  {i:>2}.   {row['town']:<30} {row['outlier_rate']:>11.2f}% "
              f"{row['outliers']:>10,} {row['count']:>8,}")

    # ==================== QUERY 10 ====================
    print_header(
        "Time-Series Trend Analysis - Quarterly Moving Averages",
        "How do average prices trend over time, and are we above or below trend?",
        "Group by quarter, compute avg price, calculate 4-quarter moving average",
        "Groupby + windowing for moving average + trend detection"
    )
    trend = quarterly_trend(records, window=4)
    print("\nLast 10 Quarters:")
    print(f"  {'Quarter':<12} {'Avg Price':>15} {'Moving Avg':>15} {'Trend':<15} {'Count':>8}")
    print("  " + "-"*75)
    for row in trend:
        ma_str = f"${row['moving_avg']:,.0f}" if row['moving_avg'] else "N/A"
        print(f"  {row['year_quarter']:<12} ${row['avg_price']:>13,.0f} "
              f"{ma_str:>15} {row['trend']:<15} {row['count']:>8,}")

    


if __name__ == "__main__":
    main()