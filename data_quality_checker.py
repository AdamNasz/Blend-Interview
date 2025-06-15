import pandas as pd
import numpy as np
from file_reader import read_customers, read_products, read_orders

try:
    customers_df = read_customers()
    products_df = read_products()
    orders_df = read_orders()
except Exception as e:
    print(f"Error loading data: {str(e)}")
    raise


def check_completeness():
    """Check for missing values and calculate completeness percentage."""
    results = {}
    for name, df in [("customers", customers_df),
                     ("products", products_df),
                     ("orders", orders_df)]:
        total_cells = df.shape[0] * df.shape[1]
        missing_cells = df.isnull().sum().sum()
        results[name] = {
            'missing_values': df.isnull().sum().to_dict(),
            'completeness_ratio': (total_cells - missing_cells) / total_cells * 100
        }
    return results

def validate_data_ranges():
    """Check if numerical values are within expected ranges."""
    issues = []

    # Basic sanity check examples
    # Check product prices
    if 'price' in products_df.columns:
        invalid_prices = products_df[products_df['price'] < 0]
        if not invalid_prices.empty:
            issues.append("Found negative prices in products")

    # Check order quantities  
    if 'quantity' in orders_df.columns:
        invalid_qty = orders_df[orders_df['quantity'] <= 0]
        if not invalid_qty.empty:
            issues.append("Found invalid quantities in orders")

    return issues


def check_uniqueness():
    """Check uniqueness constraints for key fields."""
    duplicates = {
        'customers': customers_df.duplicated().sum(),
        'products': products_df.duplicated().sum(),
        'orders': orders_df.duplicated().sum()
    }
    return duplicates


def generate_quality_report():
    """Generate comprehensive data quality report."""
    return {
        'completeness': check_completeness(),
        'range_validation': validate_data_ranges(),
        'uniqueness': check_uniqueness()
    }


try:
    report = generate_quality_report()

    print("\nData Quality Report")
    print("==================")

    print("\nCompleteness Analysis:")
    for dataset, stats in report['completeness'].items():
        print(f"\n{dataset.upper()}:")
        print(f"Completeness: {stats['completeness_ratio']:.2f}%")
        print("Missing values:", stats['missing_values'])

    print("\nData Range Issues:")
    for issue in report['range_validation']:
        print(f"- {issue}")

    print("\nDuplicate Records:")
    for dataset, count in report['uniqueness'].items():
        print(f"{dataset}: {count} duplicates")

except Exception as e:
    print(f"Error generating report: {str(e)}")
