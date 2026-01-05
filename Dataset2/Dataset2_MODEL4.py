import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import IsolationForest

# =====================
# PATHS
# =====================
data_path = "/Users/anandhytapratamaputrisutisna/FYP2/Data/dataset2_processed.csv"
results_folder = "/Users/anandhytapratamaputrisutisna/FYP2/Data/dataset2_model4_results"
os.makedirs(results_folder, exist_ok=True)

# =====================
# LOAD DATA
# =====================
df = pd.read_csv(data_path)
print("===== DATA LOADED =====")
print(df.info())
print(df.head())
print("Missing values per column:\n", df.isna().sum())

# =====================
# ANOMALY / OVERSPENDING DETECTION
# =====================
numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
iso = IsolationForest(contamination='auto', random_state=42)
df['anomaly'] = iso.fit_predict(df[numeric_cols])  # -1 = anomaly, 1 = normal

num_anomalies = (df['anomaly'] == -1).sum()
percent_anomalies = num_anomalies / len(df) * 100
anomaly_clients = df[df['anomaly'] == -1]['ID'].tolist()

# =====================
# SAVE RESULTS
# =====================
df_anomaly = df[df['anomaly'] == -1]
df_anomaly.to_csv(os.path.join(results_folder, "Dataset2_Anomalies.csv"), index=False)

iso_summary = pd.DataFrame([{
    'Model': 'IsolationForest_auto',
    '% Anomaly': percent_anomalies,
    'Sample Client IDs': anomaly_clients[:5]
}])
iso_summary.to_csv(os.path.join(results_folder, "IsolationForest_Evaluation.csv"), index=False)

# =====================
# VISUALIZATION
# =====================
# Histogram of anomaly scores
plt.figure(figsize=(6,4))
sns.histplot(df['anomaly'], bins=3, kde=False)
plt.title("Distribution of Anomalies")
plt.tight_layout()
plt.savefig(os.path.join(results_folder, "anomaly_distribution.png"))
plt.close()

# Heatmap of correlations for numeric features
plt.figure(figsize=(12,10))
sns.heatmap(df[numeric_cols].corr(), annot=True, fmt=".2f", cmap="coolwarm")
plt.title("Correlation Matrix - Dataset2")
plt.tight_layout()
plt.savefig(os.path.join(results_folder, "correlation_matrix.png"))
plt.close()

# =====================
# TERMINAL SUMMARY
# =====================
print("===== MODEL 4: Overspending / Anomaly Detection Summary =====")
print(f"Total anomalies detected: {num_anomalies}")
print(f"Percentage of anomalies: {percent_anomalies:.2f}%")
print(f"Sample anomaly client IDs: {anomaly_clients[:5]}")
print(f"Visualization and CSV results saved to: {results_folder}")

print("Model 4 training & evaluation completed successfully!")
