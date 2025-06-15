from file_reader import *
import pandas as pd



def calculate_sales_difference():
    # Read orders data
    orders_df = read_orders()

    # Calculate item-level sales 
    orders_df['item_sales'] = round(orders_df['unit_sale_price'] * orders_df['quantity'], 2)

    # Aggregate by order_id
    order_totals = orders_df.groupby('order_id').agg({
        'total_amount': 'first',
        'item_sales': 'sum'
    }).round(2)

    # Compare aggregated sales with total_amount
    order_totals['sales_difference'] = round(order_totals['total_amount'] - order_totals['item_sales'], 2)

    # Calculate percentage of non-zero differences
    nonzero_pct = (order_totals['sales_difference'] != 0).mean() * 100

    # Display results
    print("Order-level sales comparison:")
    print(order_totals[order_totals['sales_difference'] != 0])
    sale_miscalculation = f"Percentage of orders with non-zero sales difference: {nonzero_pct:.2f}%"
    print(sale_miscalculation)
    order_totals.to_csv('Output/total_sales_comparison.csv')
    return  order_totals


def analyze_orders_with_discount():
    # Read orders data
    orders_df = read_orders()

    # Calculate item-level sales 
    orders_df['item_sales'] = round(orders_df['unit_sale_price'] * orders_df['quantity'], 2)

    # Aggregate by order_id and product_id
    order_analysis = orders_df.groupby(['order_id', 'product_id']).agg({
        'total_amount': 'first',
        'item_sales': 'sum',
        'quantity': 'sum',
        'unit_sale_price': 'mean'
    }).round(2)

    # Add total item sales by order_id
    order_analysis['total_item_sales'] = order_analysis.groupby('order_id')['item_sales'].transform('sum').round(2)

    # Calculate differences and discounts
    order_analysis['sales_difference'] = round(order_analysis['total_amount'] - order_analysis['total_item_sales'], 2)
    order_analysis['discount_percentage'] = round(
        (order_analysis['sales_difference'] / order_analysis['total_item_sales']) * -100, 2)
    order_analysis['has_discount'] = order_analysis['discount_percentage'] > 0.1

    print("\nOrders with discounts:")
    print(order_analysis[order_analysis['has_discount']])

    order_analysis.to_csv('Output/order_analysis_with_discounts.csv')
    return order_analysis


# Execute both analyses
orders = calculate_sales_difference()
orders_with_discount = analyze_orders_with_discount()
print("Data read successfully!")



