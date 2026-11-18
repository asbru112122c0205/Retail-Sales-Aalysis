import pandas as pd
 
# 1. Load the data
df = pd.read_csv("retail_sales_dataset.csv")
print("Rows before cleaning:", len(df))
print("Missing values before:", df.isnull().sum().sum())
 
# 2. Remove duplicate rows
df = df.drop_duplicates()
 
# 3. Convert the date column to real dates
df["date"] = pd.to_datetime(df["date"])
 
# 4. Fill region from the store (each store always has the same region)
store_region = df.dropna(subset=["region"]).drop_duplicates("store_id").set_index("store_id")["region"]
df["region"] = df["region"].fillna(df["store_id"].map(store_region))
 
# 5. Fill quantity: work it out from sales when we can, otherwise use 1 (the most common value)
can_calculate = df["quantity"].isnull() & df[["unit_price", "discount_pct", "sales_amount"]].notnull().all(axis=1)
df.loc[can_calculate, "quantity"] = (
    df["sales_amount"] / (df["unit_price"] * (1 - df["discount_pct"] / 100))
).round()
df["quantity"] = df["quantity"].fillna(1).astype(int)
 
# 6. Fill unit_price with the typical (median) price of the same product
df["unit_price"] = df["unit_price"].fillna(df.groupby("product_id")["unit_price"].transform("median"))
 
# 7. Fill discount with 0 (no discount)
df["discount_pct"] = df["discount_pct"].fillna(0)
 
# 8. Rebuild missing sales_amount = price x quantity x (1 - discount)
missing_sales = df["sales_amount"].isnull()
df.loc[missing_sales, "sales_amount"] = (
    df["unit_price"] * df["quantity"] * (1 - df["discount_pct"] / 100)
).round(2)
 
# 9. Fill the text columns that cannot be calculated with "Unknown"
for col in ["customer_id", "customer_segment", "payment_method"]:
    df[col] = df[col].fillna("Unknown")
 
# 10. Sort by date and save
df = df.sort_values(["date", "transaction_id"]).reset_index(drop=True)
df.to_csv("retail_sales_cleaned.csv", index=False)
 
print("\nRows after cleaning:", len(df))
print("Missing values after:", df.isnull().sum().sum())
print("Duplicate rows after:", df.duplicated().sum())
print("Saved: retail_sales_cleaned.csv")
 