"""
Loads and cleans the CSV dataset.
Returns list of records (dictionaries) for functional/stream processing.
"""

import csv
from datetime import datetime
from typing import List, Dict, Any, Optional


def _parse_float(value: Optional[str], default: float = 0.0) -> float:
    """
    Helper to parse floats from strings that may contain commas or be empty.
    
    Args:
        value: String value to parse
        default: Default value if parsing fails
        
    Returns:
        Parsed float or default value
    """
    if value is None:
        return default
    text = str(value).strip().replace(",", "")
    if text == "":
        return default
    try:
        return float(text)
    except ValueError:
        return default


def load_data(csv_path: str) -> List[Dict[str, Any]]:
    """
    Load the CSV and return a list of dict records with fields:
      - town: string
      - year: int
      - quarter: int (1-4)
      - year_quarter: string (e.g., '2021-Q3')
      - sale_amount: float
      - property_type: string
      - residential_type: string
      - assessed_value: float

    Filters applied:
      - sale_amount > 0
      - sale_amount <= 10,000,000 (remove extreme outliers)
      - valid Date Recorded
      - year between 2001 and 2024 (remove garbage years)
    
    Args:
        csv_path: Path to the CSV file
        
    Returns:
        List of cleaned record dictionaries
    """
    records = []
    skipped = 0
    error_samples = []
    
    try:
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            
            for i, row in enumerate(reader, start=1):
                try:
                    sale_amount = _parse_float(row.get("Sale Amount"))
                    
                    # Skip invalid or extreme values
                    if sale_amount <= 0 or sale_amount > 10_000_000:
                        skipped += 1
                        continue

                    date_str = row.get("Date Recorded", "").strip()
                    if not date_str:
                        skipped += 1
                        continue

                    # Dataset dates look like '01/15/2019'
                    dt = datetime.strptime(date_str, "%m/%d/%Y")
                    year = dt.year

                    # IMPORTANT: keep only realistic years
                    if year < 2001 or year > 2024:
                        skipped += 1
                        continue

                    month = dt.month
                    quarter = (month - 1) // 3 + 1
                    year_quarter = f"{year}-Q{quarter}"

                    assessed_value = _parse_float(row.get("Assessed Value"))

                    records.append({
                        "town": (row.get("Town") or "").strip(),
                        "year": year,
                        "quarter": quarter,
                        "year_quarter": year_quarter,
                        "sale_amount": sale_amount,
                        "property_type": (row.get("Property Type") or "").strip(),
                        "residential_type": (row.get("Residential Type") or "").strip(),
                        "assessed_value": assessed_value,
                    })
                    
                except Exception as e:
                    skipped += 1
                    if len(error_samples) < 3:
                        error_samples.append(f"Row {i}: {str(e)[:50]}")
                    continue
        
        # Print loading summary
        print(f"✓ Loaded {len(records):,} cleaned records")
        if skipped > 0:
            print(f"  Skipped {skipped:,} invalid rows")
        if error_samples:
            print(f"  Sample errors:")
            for err in error_samples:
                print(f"    - {err}")
        
        return records
        
    except FileNotFoundError:
        print(f"✗ ERROR: File not found: {csv_path}")
        print(f"  Please ensure the CSV file exists at the specified path.")
        return []
    except Exception as e:
        print(f"✗ ERROR loading data: {e}")
        return []