import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ===============================
# CONFIG
# ===============================
INPUT_FILE = "/Users/anandhytapratamaputrisutisna/FYP2/Data/dataset1_summary.csv"
OUTPUT_DIR = "/Users/anandhytapratamaputrisutisna/FYP2/data/dataset1_model2_results"
SUBFOLDER = "automatic_contamination"
os.makedirs(os.path.join(OUTPUT_DIR, SUBFOLDER), exist_ok=True)

RANDOM_STATE = 42
FEATURES = ['total_spending', 'transaction_count', 'avg_transaction_value', 'spending_variance', 'weekend_spending_ratio']

# ===============================
# LOAD DATA
# ===============================
df = pd.read_csv(INPUT_FILE)
print("Data shape:", df.shape)

# ===============================
# SCALE FEATURES
# ===============================
X = df[FEATURES].fillna(0)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ===============================
# AUTOMATIC CONTAMINATION BASED ON SPENDING
# ===============================
spending_mean = df['total_spending'].mean()
spending_std = df['total_spending'].std()
threshold = spending_mean + 3 * spending_std
contamination = np.mean(df['total_spending'] > threshold)
print(f"Automatic contamination based on spending distribution: {contamination:.4f}")

# ===============================
# FUNCTION TO RUN ISOLATION FOREST
# ===============================
def run_isolation_forest(X_scaled, contamination, output_folder):
    print(f"\nRunning Isolation Forest ({output_folder}) contamination")
    
    iso = IsolationForest(contamination=contamination, random_state=RANDOM_STATE)
    labels = iso.fit_predict(X_scaled)
    
    temp_df = df.copy()
    temp_df['anomaly'] = labels
    temp_df['anomaly_label'] = temp_df['anomaly'].map({1:'Normal', -1:'Anomaly'})
    
    folder_path = os.path.join(OUTPUT_DIR, output_folder)
    os.makedirs(folder_path, exist_ok=True)
    
    # ===============================
    # SCATTER PLOT 2D
    # ===============================
    plt.figure(figsize=(8,5))
    sns.scatterplot(
        x='transaction_count',
        y='total_spending',
        hue='anomaly_label',
        data=temp_df,
        palette=['green','red'],
        alpha=0.6
    )
    plt.title("Isolation Forest Anomalies")
    plt.xlabel("Transaction Count")
    plt.ylabel("Total Spending")
    plt.grid(True)
    plt.savefig(os.path.join(folder_path, "anomalies_scatter.png"))
    plt.close()
    
    # ===============================
    # PCA 2D VISUALIZATION
    # ===============================
    pca = PCA(n_components=2, random_state=RANDOM_STATE)
    X_pca = pca.fit_transform(X_scaled)
    temp_df['pca1'] = X_pca[:,0]
    temp_df['pca2'] = X_pca[:,1]
    
    plt.figure(figsize=(8,6))
    sns.scatterplot(
        x='pca1', y='pca2',
        hue='anomaly_label',
        data=temp_df,
        palette=['green','red'],
        alpha=0.6
    )
    plt.title("PCA 2D Visualization of Anomalies")
    plt.xlabel("PCA Component 1")
    plt.ylabel("PCA Component 2")
    plt.grid(True)
    plt.savefig(os.path.join(folder_path, "anomalies_pca2d.png"))
    plt.close()
    
    # ===============================
    # BOXPLOTS PER FEATURE
    # ===============================
    for feature in FEATURES:
        plt.figure(figsize=(8,5))
        sns.boxplot(
            x='anomaly_label',
            y=feature,
            hue='anomaly_label',
            data=temp_df,
            palette=['green','red']
        )
        plt.title(f"{feature} by Anomaly Label")
        plt.grid(True)
        plt.savefig(os.path.join(folder_path, f"{feature}_by_anomaly.png"))
        plt.close()
    
    # ===============================
    # SUMMARY TABLE
    # ===============================
    summary = temp_df.groupby('anomaly_label')[FEATURES].agg(['mean','median','std']).round(2)
    summary.to_csv(os.path.join(folder_path, "anomaly_feature_summary.csv"))
    
    # ===============================
    # FEATURE IMPORTANCE (simplified)
    # ===============================
    feature_importance = pd.DataFrame({
        'feature': FEATURES,
        'importance': np.abs(X_scaled[labels==-1].mean(axis=0))
    }).sort_values(by='importance', ascending=False)
    feature_importance.to_csv(os.path.join(folder_path, "feature_importance.csv"), index=False)
    
    # ===============================
    # SAVE DATA
    # ===============================
    temp_df.to_csv(os.path.join(folder_path, "dataset1_isolation_forest.csv"), index=False)
    
    print(f"All results saved under: {folder_path}\n")
    return summary, feature_importance

# ===============================
# RUN PIPELINE
# ===============================
summary_auto, feature_importance_auto = run_isolation_forest(X_scaled, contamination, SUBFOLDER)

print("\n===== SUMMARY =====")
print(summary_auto)

print("\n===== FEATURE IMPORTANCE =====")
print(feature_importance_auto)

print("\nIsolation Forest Model 2 pipeline completed successfully.")
