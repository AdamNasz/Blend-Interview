import os
import pandas as pd
import numpy as np
import json
import openpyxl

input_folder = "InputData"

def read_customers():
    """Read customers xlsx file and return a pandas DataFrame."""
    files_data = {}

    # Check if folder exists
    if not os.path.exists(input_folder):
        raise FileNotFoundError(f"'{input_folder}' folder not found")
    try:
        # Try reading as Excel
        data = pd.read_excel("InputData/customers.xlsx")
    except:
        print(f"Warning: Could not read file customers.xlsx")

    return data

def read_products():
    """Read products csv file and return a pandas DataFrame."""
    files_data = {}

    # Check if folder exists
    if not os.path.exists(input_folder):
        raise FileNotFoundError(f"'{input_folder}' folder not found")
    try:
        # Try reading as csv
        data = pd.read_csv("InputData/products.csv")
    except:
        print(f"Warning: Could not read file products.csv")

    return data

def read_orders():
    """Read orders JSON file and return a pandas DataFrame."""
    files_data = {}

    # Check if folder exists
    if not os.path.exists(input_folder):
        raise FileNotFoundError(f"'{input_folder}' folder not found")
    try:
        # Try reading as JSON
        with open("InputData/orders_json.txt", 'r') as file:
            json_data = json.load(file)
        # Unnest the JSON data
        data = pd.json_normalize(json_data)
        data = data.explode('items').reset_index(drop=True)
        items = pd.json_normalize(data.pop('items'))
        data = data.join(items)

    except:
        print(f"Warning: Could not read file orders_json.txt")

    return data


