import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ===============================
# CONFIG
# ===============================
INPUT_FILE = "/Users/anandhytapratamaputrisutisna/FYP2/Data/dataset1_summary.csv"
OUTPUT_DIR = "/Users/anandhytapratamaputrisutisna/FYP2/data/dataset1_model1_results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

RANDOM_STATE = 42
FEATURES = [
    'total_spending',
    'transaction_count',
    'avg_transaction_value',
    'spending_variance',
    'weekend_spending_ratio'
]
K_RANGE = range(2, 4)

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
# SILHOUETTE BASED K SELECTION
# ===============================
best_score = -1
best_k = None

for k in K_RANGE:
    km = KMeans(n_clusters=k, random_state=RANDOM_STATE)
    labels = km.fit_predict(X_scaled)
    score = silhouette_score(X_scaled, labels)
    print(f"k={k}, silhouette score={score:.4f}")
    if score > best_score:
        best_score = score
        best_k = k

print(f"\nBest k based on silhouette score: {best_k} (score={best_score:.4f})")

# ===============================
# FUNCTION TO RUN K-MEANS PIPELINE
# ===============================
def run_kmeans_pipeline(k, folder_name):
    print(f"\nRunning K-Means with k={k}")

    # Create subfolder automatically
    RUN_DIR = os.path.join(OUTPUT_DIR, folder_name)
    os.makedirs(RUN_DIR, exist_ok=True)

    # Run K-Means
    km = KMeans(n_clusters=k, random_state=RANDOM_STATE)
    labels = km.fit_predict(X_scaled)

    temp_df = df.copy()
    temp_df['cluster'] = labels

    # Order clusters by total spending
    cluster_means = temp_df.groupby('cluster')['total_spending'].mean().sort_values()
    mapping = {old: new for new, old in enumerate(cluster_means.index)}
    temp_df['cluster_label'] = temp_df['cluster'].map(mapping)

    if k == 3:
        temp_df['cluster_label'] = temp_df['cluster_label'].map({
            0: 'Low',
            1: 'Medium',
            2: 'High'
        })

    # PCA
    pca = PCA(n_components=2, random_state=RANDOM_STATE)
    X_pca = pca.fit_transform(X_scaled)
    temp_df['pca1'] = X_pca[:, 0]
    temp_df['pca2'] = X_pca[:, 1]

    plt.figure(figsize=(8, 6))
    sns.scatterplot(
        data=temp_df,
        x='pca1',
        y='pca2',
        hue='cluster_label',
        palette='Set2',
        alpha=0.7
    )
    plt.title(f"K-Means PCA Visualization (k={k})")
    plt.grid(True)
    plt.savefig(os.path.join(RUN_DIR, "pca.png"))
    plt.close()

    # Feature boxplots
    for feature in FEATURES:
        plt.figure(figsize=(8, 5))
        sns.boxplot(
            x='cluster_label',
            y=feature,
            hue='cluster_label',
            data=temp_df,
            legend=False,
            palette='Set2'
        )
        plt.title(f"{feature} by Cluster (k={k})")
        plt.grid(True)
        plt.savefig(os.path.join(RUN_DIR, f"{feature}.png"))
        plt.close()

    # Cluster summary table
    summary = temp_df.groupby('cluster_label')[FEATURES].agg(['mean', 'median', 'std']).round(2)
    summary.to_csv(os.path.join(RUN_DIR, "cluster_summary.csv"))

    # Save clustered data
    temp_df.to_csv(os.path.join(RUN_DIR, "dataset1_kmeans.csv"), index=False)

    print(f"Results for k={k} saved in {RUN_DIR}.\n")
    return summary

# ===============================
# RUN BEST K & K=3 AUTOMATICALLY
# ===============================
summary_best = run_kmeans_pipeline(best_k, f"k{best_k}_best")
summary_k3 = run_kmeans_pipeline(3, "k3_interpretability")

print("===== SUMMARY (BEST K) =====")
print(summary_best)

print("\n===== SUMMARY (K=3 INTERPRETABILITY) =====")
print(summary_k3)

print("\nK-Means Model 1 pipeline completed successfully.")
