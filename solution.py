"""
==============================================================
Day 10 Lab: Build Your First Automated ETL Pipeline
==============================================================
Student ID: 2A202600120
Name: Luu Luong Vi Nhan

Nhiem vu:
   1. Extract:   Doc du lieu tu file JSON
   2. Validate:  Kiem tra & loai bo du lieu khong hop le
   3. Transform: Chuan hoa category + tinh gia giam 10%
   4. Load:      Luu ket qua ra file CSV
==============================================================
"""

import json
import pandas as pd
import os
import datetime

# --- CONFIGURATION ---
SOURCE_FILE = 'raw_data.json'
OUTPUT_FILE = 'processed_data.csv'


def extract(file_path):
    """Doc du lieu JSON tu file."""
    print(f"Extracting data from {file_path}...")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"Extract complete. {len(data)} records loaded from source.")
        return data
    except FileNotFoundError:
        print(f"ERROR: File {file_path} not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in {file_path}: {e}")
        return None


def validate(data):
    """Kiem tra chat luong du lieu: price > 0 va category khong rong."""
    valid_records = []
    error_count = 0

    for record in data:
        price = record.get('price', 0)
        category = record.get('category')

        try:
            price_num = float(price)
        except (TypeError, ValueError):
            error_count += 1
            print(f"  - Dropped invalid record (bad price type): {record}")
            continue

        if price_num <= 0:
            error_count += 1
            print(f"  - Dropped invalid record (price <= 0): {record}")
            continue

        if category is None or str(category).strip() == '':
            error_count += 1
            print(f"  - Dropped invalid record (empty category): {record}")
            continue

        valid_records.append(record)

    print(
        f"Validation summary: {len(valid_records)} kept, "
        f"{error_count} dropped, {error_count} invalid."
    )
    return valid_records


def transform(data):
    """Ap dung business logic: discount 10%, Title Case category, timestamp."""
    if not data:
        print("Transform: no data to transform.")
        return None

    df = pd.DataFrame(data)
    df['discounted_price'] = df['price'] * 0.9
    df['category'] = df['category'].astype(str).str.title()
    df['processed_at'] = datetime.datetime.now().isoformat()

    print(f"Transform complete. {len(df)} records processed successfully.")
    return df


def load(df, output_path):
    """Luu DataFrame ra file CSV."""
    df.to_csv(output_path, index=False)
    print(f"Data saved to {output_path}")


# ============================================================
# MAIN PIPELINE
# ============================================================
if __name__ == "__main__":
    print("=" * 50)
    print("ETL Pipeline Started...")
    print("=" * 50)

    # 1. Extract
    raw_data = extract(SOURCE_FILE)

    if raw_data:
        # 2. Validate
        clean_data = validate(raw_data)

        # 3. Transform
        final_df = transform(clean_data)

        # 4. Load
        if final_df is not None:
            load(final_df, OUTPUT_FILE)
            print(f"\nPipeline completed! {len(final_df)} records saved.")
        else:
            print("\nTransform returned None. Check your transform() function.")
    else:
        print("\nPipeline aborted: No data extracted.")
