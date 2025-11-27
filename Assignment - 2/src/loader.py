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
        value: String value to parse (e.g. "250,000" or "   300000  ")
        default: Default value if parsing fails
        
    Returns:
        Parsed float or default value
    """
    # If the value is completely missing, return the default
    if value is None:
        return default

    # Convert to string, trim spaces, and remove commas
    text = str(value).strip().replace(",", "")

    # Empty string → treat as missing → return default
    if text == "":
        return default

    # Try converting to float; on any error, return default
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
    # Final list of cleaned records that we will return
    records: List[Dict[str, Any]] = []

    # Counters for basic data-quality reporting
    skipped = 0              # how many rows we skipped
    error_samples: List[str] = []  # up to 3 example errors
    
    try:
        # Open the CSV file in text mode with UTF-8 encoding
        with open(csv_path, "r", encoding="utf-8") as f:
            # DictReader gives each row as a dict using the header row as keys
            reader = csv.DictReader(f)
            
            # Process each row one by one
            for i, row in enumerate(reader, start=1):
                try:
                    # Safely parse sale amount as float
                    sale_amount = _parse_float(row.get("Sale Amount"))
                    
                    # Skip invalid or extreme sale amounts
                    if sale_amount <= 0 or sale_amount > 10_000_000:
                        skipped += 1
                        continue

                    # Read and clean the date string
                    date_str = row.get("Date Recorded", "").strip()
                    if not date_str:
                        # If date is missing, we skip the row
                        skipped += 1
                        continue

                    # Dataset dates look like '01/15/2019'
                    dt = datetime.strptime(date_str, "%m/%d/%Y")
                    year = dt.year

                    # IMPORTANT: keep only realistic years
                    if year < 2001 or year > 2024:
                        skipped += 1
                        continue

                    # Derive quarter and year_quarter from the date
                    month = dt.month
                    # Quarter calculation: 1–3 → Q1, 4–6 → Q2, etc.
                    quarter = (month - 1) // 3 + 1
                    year_quarter = f"{year}-Q{quarter}"

                    # Safely parse assessed value (can be missing / dirty)
                    assessed_value = _parse_float(row.get("Assessed Value"))

                    # Build the cleaned record in a normalized schema
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
                    # Any unexpected error while parsing this row → skip it
                    skipped += 1
                    # Save up to 3 example errors for debugging
                    if len(error_samples) < 3:
                        error_samples.append(f"Row {i}: {str(e)[:50]}")
                    continue
        
        # Print loading summary to the console
        print(f"✓ Loaded {len(records):,} cleaned records")
        if skipped > 0:
            print(f"  Skipped {skipped:,} invalid rows")
        if error_samples:
            print(f"  Sample errors:")
            for err in error_samples:
                print(f"    - {err}")
        
        # Return the cleaned dataset
        return records
        
    except FileNotFoundError:
        # Handle case where the CSV path is wrong or file is missing
        print(f"✗ ERROR: File not found: {csv_path}")
        print(f"  Please ensure the CSV file exists at the specified path.")
        return []
    except Exception as e:
        # Catch any unexpected top-level error while loading the file
        print(f"✗ ERROR loading data: {e}")
        return []
