import pandas as pd
import numpy as np
from file_reader import read_customers


def get_lowest_available_id(df):
    """Find the lowest unused ID in the dataset."""
    existing_ids = set(df['customer_id'].dropna())
    lowest_id = 1
    while lowest_id in existing_ids:
        lowest_id += 1
    return lowest_id


def clean_customer_data():
    """Clean customer data by filling missing IDs and handling duplicates."""
    # Read customer data
    df = read_customers()

    # Fill missing customer IDs with lowest available ID
    lowest_id = get_lowest_available_id(df)
    df['customer_id'] = df['customer_id'].fillna(lowest_id)

    # Sort by registration_date and keep latest entry for duplicate IDs
    df = df.sort_values('registration_date').drop_duplicates(
        subset=['customer_id'], keep='last')

    return df

try:
    customers_df = clean_customer_data()
except Exception as e:
    print(f"Error cleaning customer data: {str(e)}")
    raise
