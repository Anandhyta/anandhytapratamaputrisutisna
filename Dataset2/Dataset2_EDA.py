import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# =====================
# LOAD DATA
# =====================
file_path = "/Users/anandhytapratamaputrisutisna/FYP2/Data/dataset 2.csv"
df2 = pd.read_csv(file_path)

print("===== DATA LOADED =====")
print("Shape:", df2.shape)
print(df2.info())
print(df2.head())

# Check missing values
print("\nMissing values per column:")
print(df2.isnull().sum())

# =====================
# FOLDER SETUP
# =====================
output_folder = "/Users/anandhytapratamaputrisutisna/FYP2/Data/dataset2_eda_summary_results"
os.makedirs(output_folder, exist_ok=True)

# =====================
# COLUMN SETUP
# =====================
income_col = 'Income (USD)'
expense_cols = ['Rent (USD)','Groceries (USD)','Eating Out (USD)','Entertainment (USD)',
                'Subscription Services (USD)','Education (USD)','Online Shopping (USD)',
                'Savings (USD)','Investments (USD)','Travel (USD)','Fitness (USD)','Miscellaneous (USD)']

# =====================
# DISTRIBUTION PLOTS
# =====================
# Income distribution
plt.figure(figsize=(8,6))
sns.histplot(df2[income_col], bins=50, kde=True)
plt.title("Income Distribution")
plt.xlabel("Income (USD)")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig(os.path.join(output_folder, "Income_Distribution.png"))
plt.close()

# Expenses distribution
for col in expense_cols:
    plt.figure(figsize=(8,6))
    sns.histplot(df2[col], bins=50, kde=True)
    plt.title(f"{col} Distribution")
    plt.xlabel(col)
    plt.ylabel("Count")
    plt.tight_layout()
    safe_name = col.replace(" (USD)","").replace(" ","_")
    plt.savefig(os.path.join(output_folder, f"{safe_name}_Distribution.png"))
    plt.close()

# =====================
# EXPENSE RATIO
# =====================
df2['Total_Expense'] = df2[expense_cols].sum(axis=1)
df2['Expense_to_Income_Ratio'] = df2['Total_Expense'] / df2[income_col]

plt.figure(figsize=(8,6))
sns.histplot(df2['Expense_to_Income_Ratio'], bins=50, kde=True)
plt.title("Expense to Income Ratio Distribution")
plt.xlabel("Expense/Income")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig(os.path.join(output_folder, "Expense_to_Income_Ratio_Distribution.png"))
plt.close()

# =====================
# CORRELATION HEATMAP
# =====================
plt.figure(figsize=(12,10))
corr = df2[[income_col]+expense_cols].corr()
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.savefig(os.path.join(output_folder, "Correlation_Heatmap.png"))
plt.close()

# =====================
# SKEWNESS DETECTION
# =====================
skewness = df2[[income_col]+expense_cols].skew()
print("\nSkewness per column:")
print(skewness)

# =====================
# MULTICOLLINEARITY DETECTION
# =====================
from statsmodels.stats.outliers_influence import variance_inflation_factor

X = df2[[income_col]+expense_cols]
vif_data = pd.DataFrame()
vif_data["feature"] = X.columns
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]

print("\nVariance Inflation Factor (VIF) per column:")
print(vif_data)

# =====================
# SAVE SUMMARY CSVS
# =====================
df2[['ID', income_col, 'Total_Expense', 'Expense_to_Income_Ratio']].to_csv(
    os.path.join(output_folder, "Dataset2_Expense_Summary.csv"), index=False)

skewness.to_csv(os.path.join(output_folder, "Dataset2_Skewness.csv"))
vif_data.to_csv(os.path.join(output_folder, "Dataset2_VIF.csv"))

print(f"\nEDA plots and summary CSVs saved to: {output_folder}")
