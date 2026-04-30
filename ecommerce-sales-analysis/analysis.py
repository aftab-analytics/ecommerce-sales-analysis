import os
import pandas as pd
import matplotlib.pyplot as plt

# STEP 1 — Load dataset

BASE_DIR = os.path.dirname(__file__)
file_path = os.path.join(BASE_DIR, "books_dataset.csv")

df = pd.read_csv(file_path)

print(df.head())

# STEP 2 — Data Cleaning
df["Price"] = df["Price"].str.replace("£", "")
df["Price"] = df["Price"].astype(float)

# STEP 3 — Analysis
print("Total books:", len(df))

print("\nRating Count:")
print(df["Rating"].value_counts())

print("\nAverage Price:", df["Price"].mean())

# STEP 4 — Visualization
rating_counts = df["Rating"].value_counts()

plt.figure(figsize=(10,6))

plt.bar(rating_counts.index, rating_counts.values)

plt.title("Books Rating Distribution")
plt.xlabel("Rating")
plt.ylabel("Number of Books")

# STEP 5 — Save Chart
plt.savefig("rating_chart.png")

plt.show()