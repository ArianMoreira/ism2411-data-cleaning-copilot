# This script cleans the messy sales dataset by:
# 1. Standardizing column names
# 2. Stripping whitespace from text columns
# 3. Handling missing values
# 4. Removing invalid rows (negative quantities or prices)
# The cleaned dataset is saved to data/processed/sales_data_clean.csv

import pandas as pd
import os

# Copilot-assisted function: load the CSV
def load_data(file_path: str):
    """
    Load the CSV file into a pandas DataFrame.
    file_path: path to the raw CSV file
    Returns a DataFrame.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file was not found: {file_path}")
    df = pd.read_csv(file_path)
    return df

# Copilot-assisted function: clean column names
def clean_column_names(df):
    """
    Standardize column names by converting to lowercase and replacing spaces with underscores.
    This makes it easier to reference columns in Python.
    """
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df

# Strip whitespace from all text columns
def strip_whitespace(df):
    """
    Remove leading and trailing whitespace from text columns
    to fix inconsistent product names and categories.
    """
    text_cols = df.select_dtypes(include='object').columns
    for col in text_cols:
        df[col] = df[col].str.strip()
    return df

# Handle missing values in numeric columns
def handle_missing_values(df):
    """
    Convert 'price' and 'qty' to numeric, then drop rows with missing values.
    This fixes empty strings or invalid numbers.
    """
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['qty'] = pd.to_numeric(df['qty'], errors='coerce')
    df = df.dropna(subset=['price', 'qty'])
    return df

# Remove rows with invalid (negative) values
def remove_invalid_rows(df):
    """
    Remove rows with negative 'price' or 'qty'.
    Negative values are considered data entry errors.
    """
    df = df[(df['price'] >= 0) & (df['qty'] >= 0)]
    return df

# Main block to run the full cleaning pipeline
if __name__ == "__main__":
    # Absolute paths to your raw and processed CSV files
    raw_path = r"C:\Users\arian\python_github_assignment\ism2411-data-cleaning-copilot\data\raw\sales_data_raw.csv"
    cleaned_path = r"C:\Users\arian\python_github_assignment\ism2411-data-cleaning-copilot\data\processed\sales_data_clean.csv"

    # Step 1: Load raw data
    df_raw = load_data(raw_path)
    print("Raw data preview:")
    print(df_raw.head())

    # Step 2: Clean column names
    df_clean = clean_column_names(df_raw)

    # Step 3: Strip whitespace from text columns
    df_clean = strip_whitespace(df_clean)

    # Step 4: Handle missing values and convert numeric columns
    df_clean = handle_missing_values(df_clean)

    # Step 5: Remove invalid rows
    df_clean = remove_invalid_rows(df_clean)

    # Step 6: Save cleaned data
    df_clean.to_csv(cleaned_path, index=False)
    print("\nCleaning complete. First few rows of cleaned data:")
    print(df_clean.head())