# ===============================
# PREPROCESSING + FEATURE ENGINEERING + AUTOMATIC EDA - DATASET 1
# Purpose: Safe parsing, cleaning, generate features, and automatic EDA for modeling
# ===============================

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.impute import SimpleImputer

# ===============================
# CONFIG
# ===============================
FILE_PATH = "/Users/anandhytapratamaputrisutisna/FYP2/Data/Dataset 1.csv"
TIME_WINDOW = 'M'  # 'M' = monthly, 'W' = weekly
OUTLIER_METHOD = 'IQR'
OUTLIER_FACTOR = 3

OUTPUT_DIR = "/Users/anandhytapratamaputrisutisna/FYP2/data"
os.makedirs(OUTPUT_DIR, exist_ok=True)
PROCESSED_FILE = os.path.join(OUTPUT_DIR, "dataset1_transactions.csv")
GROUPED_FILE   = os.path.join(OUTPUT_DIR, "dataset1_summary.csv")
EDA_OUTPUT_DIR = os.path.join(OUTPUT_DIR, "dataset1_eda_summary_plots")
os.makedirs(EDA_OUTPUT_DIR, exist_ok=True)

pd.set_option('display.float_format', lambda x: f'{x:,.4f}')

# ===============================
# LOAD DATA
# ===============================
print("===== DATA LOADED =====")
df = pd.read_csv(FILE_PATH)
print(f"Original dataset shape: {df.shape}")

# ===============================
# CLEAN AMOUNT
# ===============================
df['amount'] = df['amount'].astype(str).str.replace(r'[^0-9\.\-]', '', regex=True)
df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
print("\n[CHECK] Amount after parsing:")
print(df['amount'].describe())

# ===============================
# CLEAN DATE
# ===============================
df['date'] = pd.to_datetime(df['date'], errors='coerce')
print("\n[CHECK] Date parsing:", df['date'].min(), df['date'].max())

df.dropna(subset=['amount', 'date'], inplace=True)
print(f"\nAfter dropping missing amount/date: {df.shape[0]} rows")

# ===============================
# FILTER EXPENSES
# ===============================
df = df[df['amount'] > 0]
print(f"After filtering only expenses: {df.shape[0]} rows")

# ===============================
# REMOVE EXTREME OUTLIERS
# ===============================
if OUTLIER_METHOD == 'IQR':
    Q1 = df['amount'].quantile(0.25)
    Q3 = df['amount'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - OUTLIER_FACTOR * IQR
    upper_bound = Q3 + OUTLIER_FACTOR * IQR
    df = df[(df['amount'] >= lower_bound) & (df['amount'] <= upper_bound)]
    print(f"After removing extreme outliers: {df.shape[0]} rows")

# ===============================
# TEMPORAL FEATURES
# ===============================
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['week'] = df['date'].dt.isocalendar().week
df['day_of_week'] = df['date'].dt.dayofweek
df['is_weekend'] = df['day_of_week'].isin([5,6]).astype(int)

# ===============================
# OPTIONAL FEATURES
# ===============================
df['log_amount'] = np.log1p(df['amount'])
high_value_thresh = df['amount'].quantile(0.95)
df['is_high_value'] = df['amount'] > high_value_thresh

# ===============================
# TIME WINDOW AGGREGATION
# ===============================
df['time_window'] = df['date'].dt.to_period(TIME_WINDOW).astype(str)

# ===============================
# FEATURE ENGINEERING
# ===============================
grouped_summary = df.groupby(['client_id', 'time_window']).agg(
    total_spending=('amount', 'sum'),
    transaction_count=('amount', 'count'),
    avg_transaction_value=('amount', 'mean'),
    spending_variance=('amount', 'var'),
    max_amount=('amount', 'max'),
    min_amount=('amount', 'min'),
    weekend_spending_total=('amount', lambda x: x[df.loc[x.index,'is_weekend']==1].sum())
).reset_index()

# Weekend ratio
grouped_summary['weekend_spending_ratio'] = grouped_summary['weekend_spending_total'] / grouped_summary['total_spending']
grouped_summary.drop(columns=['weekend_spending_total'], inplace=True)

# Category ratio (if category exists)
if 'category' in df.columns:
    categories = df['category'].dropna().unique()
    for cat in categories:
        cat_sum = df[df['category']==cat].groupby(['client_id','time_window'])['amount'].sum()
        grouped_summary = grouped_summary.merge(cat_sum.rename(f'ratio_{cat}'), on=['client_id','time_window'], how='left')
        grouped_summary[f'ratio_{cat}'] = grouped_summary[f'ratio_{cat}'] / grouped_summary['total_spending']
    grouped_summary.fillna(0, inplace=True)

# ===============================
# FINAL NUMERICAL IMPUTATION (FOR MODELING)
# ===============================
numeric_cols = [
    'total_spending',
    'transaction_count',
    'avg_transaction_value',
    'spending_variance',
    'max_amount',
    'min_amount',
    'weekend_spending_ratio'
]

# Report missing values before
print("\n===== MISSING VALUES BEFORE IMPUTATION =====")
print(grouped_summary[numeric_cols].isna().sum())

# Median imputation (robust for financial data)
imputer = SimpleImputer(strategy='median')
grouped_summary[numeric_cols] = imputer.fit_transform(
    grouped_summary[numeric_cols]
)

# Safety check
assert grouped_summary[numeric_cols].isna().sum().sum() == 0, \
    "❌ NaN still exists after imputation!"

print("\n✅ Missing values handled using median imputation.")


# ===============================
# SAVE CSV
# ===============================
df.to_csv(PROCESSED_FILE, index=False)
grouped_summary.to_csv(GROUPED_FILE, index=False)

print("\n===== PREPROCESSING + FEATURE ENGINEERING COMPLETE =====")
print(f"Processed transaction data saved to: {PROCESSED_FILE}")
print(f"Grouped summary saved to: {GROUPED_FILE}")
print(f"Processed rows: {df.shape[0]}")
print(f"Grouped summary shape: {grouped_summary.shape}")

# ===============================
# AUTOMATIC EDA ON GROUPED DATA
# ===============================
numeric_cols = [
    'total_spending', 'transaction_count', 'avg_transaction_value', 'spending_variance',
    'max_amount', 'min_amount', 'weekend_spending_ratio'
]

# Basic stats
print("\n===== GROUPED DATA FEATURE SUMMARY =====")
print(grouped_summary.describe())

# Histograms
for col in numeric_cols:
    if col in grouped_summary.columns:
        plt.figure(figsize=(6,4))
        sns.histplot(grouped_summary[col], bins=50, kde=True)
        plt.title(f'Distribution of {col}')
        plt.xlabel(col)
        plt.ylabel('Frequency')
        plt.tight_layout()
        plt.savefig(os.path.join(EDA_OUTPUT_DIR, f'distribution_{col}.png'))
        plt.close()

# Outlier check (3*IQR)
print("\n===== EXTREME OUTLIERS CHECK =====")
for col in numeric_cols:
    if col in grouped_summary.columns:
        q1 = grouped_summary[col].quantile(0.25)
        q3 = grouped_summary[col].quantile(0.75)
        iqr = q3 - q1
        outliers = grouped_summary[(grouped_summary[col] < q1 - 3*iqr) | (grouped_summary[col] > q3 + 3*iqr)]
        print(f"{col}: {len(outliers)} extreme outliers")

# Correlation heatmap
plt.figure(figsize=(10,8))
sns.heatmap(grouped_summary[numeric_cols].corr(), annot=True, fmt=".2f", cmap='coolwarm')
plt.title("Feature Correlation Matrix")
plt.tight_layout()
plt.savefig(os.path.join(EDA_OUTPUT_DIR, 'correlation_matrix.png'))
plt.close()

print(f"\n===== PREPROCESSING COMPLETE =====")
print(f"EDA plots saved under: {EDA_OUTPUT_DIR}")
