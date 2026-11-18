import pandas as pd
import matplotlib.pyplot as plt
 
# Load the cleaned data
df = pd.read_csv("retail_sales_cleaned.csv", parse_dates=["date"])
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
 
# 1. Line chart: monthly sales trend (the main chart for forecasting)
plt.figure(figsize=(10, 5))
monthly = df.groupby(df["date"].dt.to_period("M"))["sales_amount"].sum()
plt.plot(monthly.index.to_timestamp(), monthly.values, marker="o", color="steelblue")
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.grid(True)
plt.tight_layout()
plt.savefig("retail_chart1_monthly_trend.png")
plt.show()
 
# 2. Line chart: seasonality (each year as its own line)
plt.figure(figsize=(10, 5))
by_year_month = df.groupby(["month", "year"])["sales_amount"].sum().unstack()
for year in by_year_month.columns:
    plt.plot(by_year_month.index, by_year_month[year], marker="o", label=year)
plt.title("Sales by Month for Each Year (Seasonality)")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.xticks(range(1, 13))
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("retail_chart2_seasonality.png")
plt.show()
 
# 3. Bar chart: total sales by category
plt.figure()
df.groupby("category")["sales_amount"].sum().sort_values().plot(kind="barh", color="orange")
plt.title("Total Sales by Category")
plt.xlabel("Sales")
plt.tight_layout()
plt.savefig("retail_chart3_category.png")
plt.show()
 
# 4. Bar chart: total sales by region
plt.figure()
df.groupby("region")["sales_amount"].sum().sort_values(ascending=False).plot(kind="bar", color="green")
plt.title("Total Sales by Region")
plt.xlabel("Region")
plt.ylabel("Sales")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("retail_chart4_region.png")
plt.show()
 
# 5. Bar chart: average daily sales by day of the week
plt.figure()
daily = df.groupby("date")["sales_amount"].sum().reset_index()
daily["weekday"] = daily["date"].dt.day_name()
order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
daily.groupby("weekday")["sales_amount"].mean().reindex(order).plot(kind="bar", color="purple")
plt.title("Average Daily Sales by Day of the Week")
plt.xlabel("Day")
plt.ylabel("Average daily sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("retail_chart5_weekday.png")
plt.show()
 
# 6. Pie chart: share of sales by payment method
plt.figure()
pay = df.groupby("payment_method")["sales_amount"].sum()
plt.pie(pay, labels=pay.index, autopct="%1.1f%%", startangle=90)
plt.title("Sales Share by Payment Method")
plt.tight_layout()
plt.savefig("retail_chart6_payment.png")
plt.show()
 