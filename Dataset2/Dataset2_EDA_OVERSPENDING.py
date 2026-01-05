import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# =====================
# PATHS
# =====================
data_path = "/Users/anandhytapratamaputrisutisna/FYP2/Data/dataset2_processed.csv"
eda_folder = "/Users/anandhytapratamaputrisutisna/FYP2/Data/dataset2_eda_overspending"
os.makedirs(eda_folder, exist_ok=True)

# =====================
# LOAD DATA
# =====================
df = pd.read_csv(data_path)
print("===== DATA LOADED =====")
print(df.info())
print(df.head())

# =====================
# DERIVED FEATURES FOR OVERSPENDING
# =====================
# Pastikan fitur ini sudah ada, kalau belum buat
if 'total_expense' not in df.columns:
    df['total_expense'] = df[['Rent (USD)', 'Groceries (USD)', 'Eating Out (USD)',
                              'Entertainment (USD)', 'Subscription Services (USD)',
                              'Education (USD)', 'Online Shopping (USD)',
                              'Travel (USD)', 'Fitness (USD)', 'Miscellaneous (USD)']].sum(axis=1)

if 'expense_to_income_ratio' not in df.columns:
    df['expense_to_income_ratio'] = df['total_expense'] / df['Income (USD)']

if 'discretionary_vs_fixed_ratio' not in df.columns:
    df['discretionary_vs_fixed_ratio'] = (
        df[['Eating Out (USD)', 'Entertainment (USD)',
            'Subscription Services (USD)', 'Online Shopping (USD)',
            'Travel (USD)', 'Fitness (USD)', 'Miscellaneous (USD)']].sum(axis=1)
        / df[['Rent (USD)', 'Groceries (USD)', 'Education (USD)']].sum(axis=1)
    )

if 'savings_rate' not in df.columns:
    df['savings_rate'] = df['Savings (USD)'] / df['Income (USD)']

# =====================
# BASIC STATISTICS
# =====================
print("Summary Statistics for Derived Features:")
print(df[['savings_rate', 'expense_to_income_ratio', 'discretionary_vs_fixed_ratio']].describe())

# =====================
# PLOTS - DISTRIBUTIONS
# =====================
for col in ['savings_rate', 'expense_to_income_ratio', 'discretionary_vs_fixed_ratio']:
    plt.figure(figsize=(6,4))
    sns.histplot(df[col], bins=50, kde=True)
    plt.title(f'Distribution of {col}')
    plt.xlabel(col)
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.savefig(os.path.join(eda_folder, f'{col}_distribution.png'))
    plt.close()

# =====================
# PLOTS - TOP CONTRIBUTORS TO EXPENSES
# =====================
expense_cols = ['Rent (USD)', 'Groceries (USD)', 'Eating Out (USD)',
                'Entertainment (USD)', 'Subscription Services (USD)',
                'Education (USD)', 'Online Shopping (USD)',
                'Travel (USD)', 'Fitness (USD)', 'Miscellaneous (USD)']

# Mean contribution per category
mean_expenses = df[expense_cols].mean().sort_values(ascending=False)
plt.figure(figsize=(10,6))
sns.barplot(x=mean_expenses.values, y=mean_expenses.index)
plt.title("Average Expense per Category")
plt.xlabel("Average USD")
plt.ylabel("Category")
plt.tight_layout()
plt.savefig(os.path.join(eda_folder, "average_expense_per_category.png"))
plt.close()

# =====================
# CORRELATION WITH EXPENSE TO INCOME RATIO
# =====================
corr_with_exp_ratio = df[expense_cols + ['expense_to_income_ratio']].corr()['expense_to_income_ratio'].sort_values(ascending=False)
plt.figure(figsize=(10,6))
sns.barplot(x=corr_with_exp_ratio.values, y=corr_with_exp_ratio.index)
plt.title("Correlation of Each Expense Category with Expense-to-Income Ratio")
plt.xlabel("Correlation")
plt.ylabel("Category")
plt.tight_layout()
plt.savefig(os.path.join(eda_folder, "correlation_expense_to_income.png"))
plt.close()

# =====================
# HIGHLIGHT TOP FEATURES CONTRIBUTING TO OVERSPENDING
# =====================
top_features = corr_with_exp_ratio.drop('expense_to_income_ratio').head(5)
print("\nTop 5 Expense Categories Driving Overspending:")
print(top_features)

print(f"\nEDA + Feature Analysis for Overspending saved to folder: {eda_folder}")
