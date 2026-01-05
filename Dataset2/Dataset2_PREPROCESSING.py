import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.decomposition import PCA
from statsmodels.stats.outliers_influence import variance_inflation_factor

# =====================
# PATHS
# =====================
data_path = "/Users/anandhytapratamaputrisutisna/FYP2/Data/Dataset 2.csv"
processed_path = "/Users/anandhytapratamaputrisutisna/FYP2/Data/dataset2_processed.csv"
scaled_path = "/Users/anandhytapratamaputrisutisna/FYP2/Data/dataset2_scaled.csv"
eda_results_folder = "/Users/anandhytapratamaputrisna/FYP2/Data/dataset2_eda_summary_results"
anomaly_folder = "/Users/anandhytapratamaputrisutisna/FYP2/Data/dataset2_anomaly_results"

# to make sure anomaly results can be saved
os.makedirs(anomaly_folder, exist_ok=True)

# =====================
# LOAD DATA
# =====================
df = pd.read_csv(data_path)
print("===== DATA LOADED =====")
print(df.info())
print(df.head())
print("Missing values per column:\n", df.isna().sum())

# =====================
# PREPROCESSING + FEATURE ENGINEERING
# =====================
# Derived features
expense_cols = ['Rent (USD)', 'Groceries (USD)', 'Eating Out (USD)',
                'Entertainment (USD)', 'Subscription Services (USD)',
                'Education (USD)', 'Online Shopping (USD)',
                'Travel (USD)', 'Fitness (USD)', 'Miscellaneous (USD)']

discretionary_cols = ['Eating Out (USD)', 'Entertainment (USD)',
                      'Subscription Services (USD)', 'Online Shopping (USD)',
                      'Travel (USD)', 'Fitness (USD)', 'Miscellaneous (USD)']

fixed_cols = ['Rent (USD)', 'Groceries (USD)', 'Education (USD)']

df['total_expense'] = df[expense_cols].sum(axis=1)
df['savings_rate'] = df['Savings (USD)'] / df['Income (USD)']
df['expense_to_income_ratio'] = df['total_expense'] / df['Income (USD)']
df['discretionary_vs_fixed_ratio'] = df[discretionary_cols].sum(axis=1) / df[fixed_cols].sum(axis=1)

# Fill missing numeric values (median)
numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

# Save processed CSV
df.to_csv(processed_path, index=False)
print(f"Processed CSV saved to: {processed_path}")

# =====================
# SCALING
# =====================
scaler = StandardScaler()
df_scaled = df.copy()
df_scaled[numeric_cols] = scaler.fit_transform(df[numeric_cols])
df_scaled.to_csv(scaled_path, index=False)
print(f"Scaled CSV saved to: {scaled_path}")

# =====================
# ANOMALY / OVERSPENDING DETECTION
# =====================
iso = IsolationForest(contamination='auto', random_state=42)
df['anomaly'] = iso.fit_predict(df[numeric_cols])  # -1 = anomaly, 1 = normal

num_anomalies = (df['anomaly'] == -1).sum()
anomaly_clients = df[df['anomaly'] == -1]['ID'].tolist()
df_anomaly_trans = df[df['ID'].isin(anomaly_clients)]

# Save anomaly results
df_anomaly_trans.to_csv(os.path.join(anomaly_folder, "Sample_Anomalous_Transactions.csv"), index=False)
iso_summary = pd.DataFrame([{
    'Model': 'IsolationForest_auto',
    '% Anomaly': num_anomalies / len(df) * 100,
    'Sample Client IDs': anomaly_clients[:5]
}])
iso_summary.to_csv(os.path.join(anomaly_folder, "IsolationForest_Dataset2_Evaluation.csv"), index=False)
print(f"Anomaly detection results saved to: {anomaly_folder}")

# =====================
# PCA Visualization (Optional)
# =====================
pca = PCA(n_components=2)
X_pca = pca.fit_transform(df_scaled[numeric_cols])
df['PCA1'] = X_pca[:,0]
df['PCA2'] = X_pca[:,1]

# Static PCA plot
plt.figure(figsize=(8,6))
sns.scatterplot(
    data=df, x='PCA1', y='PCA2',
    hue='anomaly', palette={1:'green', -1:'red'},
    alpha=0.7
)
plt.title("PCA of Dataset2 with Anomalies")
plt.tight_layout()
plt.savefig(os.path.join(anomaly_folder, "PCA_Static.png"))
plt.close()

print("Preprocessing for Dataset2 completed successfully!")
