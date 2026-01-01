# data_cleaning_visuals.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------------
# Step 1: Load Dataset
# -------------------------------
file_path = "sales_data.csv"  # replace with your path
df= pd.read_csv(file_path, encoding='cp1252')  # or encoding='latin1'


print("Initial Dataset Info:")
print(df.info())
print(df.head())

# -------------------------------
# Step 2: Visualize Missing Values Before Cleaning
# -------------------------------
plt.figure(figsize=(12,6))
sns.heatmap(df.isnull(), cbar=False, yticklabels=False, cmap='viridis')
plt.title("Missing Values Before Cleaning")
plt.show()

# -------------------------------
# Step 3: Remove Duplicates
# -------------------------------
duplicates = df.duplicated()
print(f"\nNumber of duplicate rows: {duplicates.sum()}")
df = df.drop_duplicates()
print("Duplicates removed.")

# -------------------------------
# Step 4: Handle Missing Values
# -------------------------------
# Fill numeric with median
numeric_cols = ['QUANTITYORDERED', 'PRICEEACH', 'SALES', 'MSRP']
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

# Fill categorical with mode
categorical_cols = ['PRODUCTLINE', 'COUNTRY', 'DEALSIZE']
for col in categorical_cols:
    df[col] = df[col].fillna(df[col].mode()[0])

# -------------------------------
# Step 5: Fix Wrong Data Types
# -------------------------------
df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'], errors='coerce')
df['QUANTITYORDERED'] = pd.to_numeric(df['QUANTITYORDERED'], errors='coerce')
df['PRICEEACH'] = pd.to_numeric(df['PRICEEACH'], errors='coerce')
df['SALES'] = pd.to_numeric(df['SALES'], errors='coerce')

# -------------------------------
# Step 6: Handle Outliers
# -------------------------------
sales_mean = df['SALES'].mean()
sales_std = df['SALES'].std()
df = df[df['SALES'] <= (sales_mean + 3 * sales_std)]
print("\nOutliers removed based on SALES column.")

# -------------------------------
# Step 7: Visualizations After Cleaning
# -------------------------------

# 1. Distribution of SALES before and after cleaning
plt.figure(figsize=(12,5))
sns.histplot(df['SALES'], bins=50, kde=True, color='green')
plt.title("Sales Distribution After Cleaning")
plt.xlabel("Sales")
plt.show()

# 2. Count of missing values after cleaning
plt.figure(figsize=(12,6))
sns.heatmap(df.isnull(), cbar=False, yticklabels=False, cmap='viridis')
plt.title("Missing Values After Cleaning")
plt.show()

# 3. Boxplot to check outliers removed
plt.figure(figsize=(10,6))
sns.boxplot(df['SALES'], color='orange')
plt.title("Sales Boxplot After Cleaning")
plt.show()

# -------------------------------
# Step 8: Save Cleaned Dataset
# -------------------------------
df.to_csv("sales_data_cleaned_visuals.csv", index=False)
print("\nCleaned dataset saved as 'sales_data_cleaned_visuals.csv'")
