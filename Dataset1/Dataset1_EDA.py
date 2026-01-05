import pandas as pd
import numpy as np

# ===============================
# CONFIG
# ===============================
FILE_PATH = "Dataset1/Dataset1.csv"  
SAMPLE_SIZE = 500_000

pd.set_option('display.float_format', lambda x: f'{x:,.4f}')

# ===============================
# LOAD DATA
# ===============================
print("===== DATA LOADED =====")
df = pd.read_csv("/Users/anandhytapratamaputrisutisna/FYP2/Data/Dataset 1.csv")

# ===============================
# EDA PART 1 — STRUCTURAL CHECK
# ===============================
print("\n[EDA 1] Shape (rows, columns):")
print(df.shape)

# Missing values
missing = pd.DataFrame({
    'missing_count': df.isna().sum(),
    'missing_percentage': df.isna().mean() * 100
}).sort_values('missing_percentage', ascending=False)

print("\n[EDA 1] Missing Values:")
print(missing)

# Unique users
print("\n[EDA 1] Unique Users:")
print("Number of unique users:", df['client_id'].nunique())

# ===============================
# CLEANING — AMOUNT
# ===============================
print("\n[CLEANING] Cleaning amount column...")
df['amount'] = pd.to_numeric(df['amount'], errors='coerce')

print("Amount dtype after cleaning:", df['amount'].dtype)
print("NaN amount count:", df['amount'].isna().sum())
print(df['amount'].describe())

# ===============================
# TIME COLUMN
# ===============================
df['date'] = pd.to_datetime(df['date'], errors='coerce')

print("\n[EDA 1] Time Range:")
print("Start date:", df['date'].min())
print("End date:", df['date'].max())

# ===============================
# EDA PART 2 — SAMPLING
# ===============================
print("\n===== EDA PART 2 =====")
sample_df = df.sample(SAMPLE_SIZE, random_state=42)
print("\n[EDA 2.1] Sample shape:", sample_df.shape)

# ===============================
# EDA PART 3 — USER LEVEL BEHAVIOR
# ===============================
user_stats = df.groupby('client_id').agg(
    total_transactions=('id', 'count'),
    total_amount=('amount', 'sum'),
    avg_amount=('amount', 'mean')
)

print("\n[EDA 2.3] User Statistics Summary:")
print(user_stats.describe())

# ===============================
# EDA PART 4 — SPENDING VS REFUND
# ===============================
spending = df[df['amount'] > 0]
refunds = df[df['amount'] < 0]

print("\n[EDA 3.1] Spending vs Refund Counts:")
print({
    'spending_tx': len(spending),
    'refund_tx': len(refunds)
})

print("\n[EDA 3.2] Spending Amount Summary:")
print(spending['amount'].describe())

print("\n[EDA 3.3] Refund Amount Summary:")
print(refunds['amount'].describe())

# ===============================
# EDA PART 5 — MCC ANALYSIS
# ===============================
print("\n[EDA 2.5] Top 10 MCC Codes:")
print(df['mcc'].value_counts().head(10))

mcc_value = df.groupby('mcc')['amount'].sum().sort_values(ascending=False)
print("\n[EDA 4.1] Top 10 MCC by Total Value:")
print(mcc_value.head(10))

# ===============================
# EDA PART 6 — ERROR SIGNAL
# ===============================
df['has_error'] = df['errors'].notna()

print("\n[EDA 2.6] Error Signal Proportion:")
print(df['has_error'].value_counts(normalize=True))

# ===============================
# EDA PART 7 — TEMPORAL BEHAVIOR
# ===============================
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month

yearly_tx = df.groupby('year').size()
yearly_amount = df.groupby('year')['amount'].sum()

print("\n[EDA 5.1] Transactions per Year:")
print(yearly_tx)

print("\n[EDA 5.2] Total Amount per Year:")
print(yearly_amount)

# ===============================
# EDA PART 8 — USER SEGMENTATION
# ===============================
user_stats['segment'] = pd.qcut(
    user_stats['total_transactions'],
    q=[0, 0.33, 0.66, 1.0],
    labels=['Low', 'Medium', 'Power']
)

print("\n[EDA 6.1] User Segmentation Counts:")
print(user_stats['segment'].value_counts())

# ===============================
# EDA PART 9 — OUTLIER CHECK
# ===============================
q1 = df['amount'].quantile(0.25)
q3 = df['amount'].quantile(0.75)
iqr = q3 - q1

outliers = df[(df['amount'] < q1 - 3 * iqr) | (df['amount'] > q3 + 3 * iqr)]

print("\n[EDA 7.1] Extreme Outliers Count:")
print(len(outliers))

# ===============================
# FINAL SUMMARY
# ===============================
print("\n===== FULL EDA COMPLETE (MODELING READY) =====")
          