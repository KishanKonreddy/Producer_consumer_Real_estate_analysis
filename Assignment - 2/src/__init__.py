"""
Real Estate Sales Analysis Package
"""

__version__ = "1.0.0"

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

__all__ = [
    "load_data",
    "yearly_sales_summary",
    "top_towns_by_total_sales",
    "residential_type_stats",
    "price_to_assessed_ratio",
    "total_sales_all",
    "total_sales_year",
    "top_towns_by_average_price",
    "price_distribution",
    "outlier_towns",
    "quarterly_trend",
]