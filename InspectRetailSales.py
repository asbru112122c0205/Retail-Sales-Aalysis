import pandas as pd
 
# Load the data
df = pd.read_csv("retail_sales_dataset.csv")
 
print("Shape (rows, columns):", df.shape)
print("\nColumn names and types:\n", df.dtypes)
print("\nFirst 5 rows:\n", df.head())
 
# Missing values (nulls) in each column
print("\nMissing values:\n", df.isnull().sum())
 
# Duplicate rows
print("\nDuplicate rows:", df.duplicated().sum())
 
# Convert the date column and check the date range
df["date"] = pd.to_datetime(df["date"])
print("\nDate range:", df["date"].min(), "to", df["date"].max())
 
# Summary of the number columns
print("\nSummary of numbers:\n", df[["unit_price", "quantity", "discount_pct", "sales_amount"]].describe())
 
# Quick look at categories and sales
print("\nRows per category:\n", df["category"].value_counts())
print("\nSales by category:\n", df.groupby("category")["sales_amount"].sum())