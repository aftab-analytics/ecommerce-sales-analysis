import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# STEP 1 — Load dataset
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "books_data.csv")

df = pd.read_csv(file_path)

print("="*50)
print("🛍️  ECOMMERCE SALES ANALYSIS")
print("="*50)

print("\n📋 First 5 rows:")
print(df.head())

print("\n📊 Dataset Info:")
print(f"Total rows: {len(df)}")
print(f"Columns: {list(df.columns)}")

# STEP 2 — Data Cleaning & Preparation
print("\n🔧 Data Cleaning...")

# Check if any missing values
print(f"Missing values:\n{df.isnull().sum()}")

# Calculate Total Sales (Price × Quantity)
df['Total_Sales'] = df['Price'] * df['Quantity']
print("✅ Added 'Total_Sales' column")

# STEP 3 — Analysis

print("\n" + "="*50)
print("📈 SALES ANALYSIS REPORT")
print("="*50)

# Basic statistics
print(f"\n💰 Price Statistics:")
print(f"   Average Price: £{df['Price'].mean():.2f}")
print(f"   Most Expensive: £{df['Price'].max():.2f}")
print(f"   Cheapest: £{df['Price'].min():.2f}")

print(f"\n📦 Quantity Statistics:")
print(f"   Average Quantity: {df['Quantity'].mean():.1f}")
print(f"   Total Items Sold: {df['Quantity'].sum()}")
print(f"   Max in Single Order: {df['Quantity'].max()}")

print(f"\n💵 Revenue Statistics:")
print(f"   Total Revenue: £{df['Total_Sales'].sum():,.2f}")
print(f"   Average Order Value: £{df['Total_Sales'].mean():.2f}")
print(f"   Highest Order: £{df['Total_Sales'].max():.2f}")

# Category Analysis
print(f"\n📂 Category Analysis:")
category_sales = df.groupby('Category').agg({
    'Quantity': 'sum',
    'Total_Sales': 'sum',
    'Product': 'count'
}).rename(columns={'Product': 'Orders'})

category_sales['Revenue_Percentage'] = (category_sales['Total_Sales'] / category_sales['Total_Sales'].sum()) * 100

print(category_sales.round(2))

# Top Products
print(f"\n🏆 Top 5 Products by Revenue:")
top_products = df.groupby('Product').agg({
    'Total_Sales': 'sum',
    'Quantity': 'sum'
}).sort_values('Total_Sales', ascending=False).head(5)

print(top_products.round(2))

# STEP 4 — Visualizations
print("\n" + "="*50)
print("📊 GENERATING VISUALIZATIONS")
print("="*50)

# Create a figure with 4 subplots
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Ecommerce Sales Dashboard', fontsize=16, fontweight='bold')

# Plot 1: Sales by Category (Bar Chart)
category_revenue = df.groupby('Category')['Total_Sales'].sum().sort_values()
axes[0, 0].barh(category_revenue.index, category_revenue.values, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
axes[0, 0].set_xlabel('Revenue (£)')
axes[0, 0].set_title('Revenue by Category', fontsize=12, fontweight='bold')
for i, v in enumerate(category_revenue.values):
    axes[0, 0].text(v + 5, i, f'£{v:,.0f}', va='center')

# Plot 2: Category Distribution (Pie Chart)
category_orders = df['Category'].value_counts()
axes[0, 1].pie(category_orders.values, labels=category_orders.index, autopct='%1.1f%%', startangle=90)
axes[0, 1].set_title('Order Distribution by Category', fontsize=12, fontweight='bold')

# Plot 3: Price vs Quantity (Scatter Plot)
scatter = axes[1, 0].scatter(df['Price'], df['Quantity'], c=df['Total_Sales'], cmap='viridis', s=50, alpha=0.6)
axes[1, 0].set_xlabel('Price (£)')
axes[1, 0].set_ylabel('Quantity')
axes[1, 0].set_title('Price vs Quantity (Color = Total Sales)', fontsize=12, fontweight='bold')
plt.colorbar(scatter, ax=axes[1, 0], label='Total Sales (£)')

# Plot 4: Daily Sales Trend (if Date column exists)
if 'Date' in df.columns:
    df['Date'] = pd.to_datetime(df['Date'])
    daily_sales = df.groupby('Date')['Total_Sales'].sum()
    axes[1, 1].plot(daily_sales.index, daily_sales.values, marker='o', linewidth=2, markersize=6)
    axes[1, 1].set_xlabel('Date')
    axes[1, 1].set_ylabel('Revenue (£)')
    axes[1, 1].set_title('Daily Sales Trend', fontsize=12, fontweight='bold')
    axes[1, 1].grid(True, alpha=0.3)
    plt.setp(axes[1, 1].xaxis.get_majorticklabels(), rotation=45)
else:
    # If no Date column, show top products instead
    top_products_plot = df.groupby('Product')['Total_Sales'].sum().sort_values(ascending=True).tail(5)
    axes[1, 1].barh(top_products_plot.index, top_products_plot.values, color='lightcoral')
    axes[1, 1].set_xlabel('Revenue (£)')
    axes[1, 1].set_title('Top 5 Products by Revenue', fontsize=12, fontweight='bold')
    for i, v in enumerate(top_products_plot.values):
        axes[1, 1].text(v + 5, i, f'£{v:,.0f}', va='center')

plt.tight_layout()
plt.savefig("ecommerce_dashboard.png", dpi=150, bbox_inches='tight')
print("✅ Dashboard saved as 'ecommerce_dashboard.png'")

# STEP 5 — Additional Charts (Individual)
print("\n📈 Creating individual charts...")

# Chart 1: Sales by Category (Bar Chart)
plt.figure(figsize=(10, 6))
category_counts = df['Category'].value_counts()
plt.bar(category_counts.index, category_counts.values, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
plt.title('Number of Orders by Category', fontsize=14, fontweight='bold')
plt.xlabel('Category', fontsize=12)
plt.ylabel('Number of Orders', fontsize=12)
plt.grid(True, alpha=0.3)
for i, v in enumerate(category_counts.values):
    plt.text(i, v + 0.5, str(v), ha='center', fontsize=10)
plt.savefig("category_orders.png", dpi=100, bbox_inches='tight')
plt.show()

# Chart 2: Price Distribution (Histogram)
plt.figure(figsize=(10, 6))
plt.hist(df['Price'], bins=15, color='lightblue', edgecolor='black', alpha=0.7)
plt.title('Product Price Distribution', fontsize=14, fontweight='bold')
plt.xlabel('Price (£)', fontsize=12)
plt.ylabel('Number of Products', fontsize=12)
plt.grid(True, alpha=0.3)
plt.savefig("price_distribution.png", dpi=100, bbox_inches='tight')
plt.show()

# STEP 6 — Export Results
print("\n" + "="*50)
print("📁 EXPORTING RESULTS")
print("="*50)

# Save analysis results to CSV
category_sales.to_csv('category_analysis.csv')
print("✅ Category analysis saved to 'category_analysis.csv'")

# Summary report as text file
with open('sales_report.txt', 'w') as f:
    f.write("ECOMMERCE SALES ANALYSIS REPORT\n")
    f.write("="*40 + "\n\n")
    f.write(f"Total Orders: {len(df)}\n")
    f.write(f"Total Revenue: £{df['Total_Sales'].sum():,.2f}\n")
    f.write(f"Average Order Value: £{df['Total_Sales'].mean():.2f}\n\n")
    f.write("Category Breakdown:\n")
    f.write(category_sales.to_string())
    
print("✅ Sales report saved to 'sales_report.txt'")

print("\n" + "="*50)
print("✅ ANALYSIS COMPLETED SUCCESSFULLY!")
print("="*50)
print("\n📂 Generated Files:")
print("   1. ecommerce_dashboard.png (Main dashboard)")
print("   2. category_orders.png (Category chart)")
print("   3. price_distribution.png (Price histogram)")
print("   4. category_analysis.csv (Category data)")
print("   5. sales_report.txt (Summary report)")