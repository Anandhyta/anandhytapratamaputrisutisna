import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

# =====================
# PATHS
# =====================
data_path = "/Users/anandhytapratamaputrisutisna/FYP2/Data/dataset2_processed.csv"  # pake versi processed, bukan scaled
results_folder = "/Users/anandhytapratamaputrisutisna/FYP2/Data/dataset2_model5_results"
os.makedirs(results_folder, exist_ok=True)

# =====================
# LOAD DATA
# =====================
df = pd.read_csv(data_path)
print("===== DATA LOADED =====")
print(df.info())
print(df.head())

# =====================
# SELECT FEATURES FOR CLUSTERING
# =====================
# gunakan hanya numeric expense-related columns (tanpa ID)
expense_cols = ['Rent (USD)', 'Groceries (USD)', 'Eating Out (USD)', 
                'Entertainment (USD)', 'Subscription Services (USD)',
                'Education (USD)', 'Online Shopping (USD)',
                'Travel (USD)', 'Fitness (USD)', 'Miscellaneous (USD)',
                'total_expense', 'savings_rate', 'expense_to_income_ratio', 
                'discretionary_vs_fixed_ratio']

X = df[expense_cols]

# =====================
# SCALE FEATURES
# =====================
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# =====================
# OPTIONAL PCA FOR DIMENSIONALITY REDUCTION / VISUALIZATION
# =====================
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
df['PCA1'] = X_pca[:,0]
df['PCA2'] = X_pca[:,1]

# =====================
# KMEANS CLUSTERING
# =====================
n_clusters = 4
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
df['cluster'] = kmeans.fit_predict(X_scaled)

# =====================
# SAVE CLUSTERED DATA
# =====================
df.to_csv(os.path.join(results_folder, "dataset2_clustered.csv"), index=False)

# =====================
# CLUSTER SUMMARY
# =====================
cluster_summary = df.groupby('cluster')[expense_cols].mean()
cluster_summary.to_csv(os.path.join(results_folder, "KMeans_Cluster_Summary.csv"))
print(f"Cluster summary saved to: {results_folder}/KMeans_Cluster_Summary.csv")

# =====================
# PCA VISUALIZATION
# =====================
plt.figure(figsize=(8,6))
sns.scatterplot(
    data=df, x='PCA1', y='PCA2',
    hue='cluster', palette='tab10', alpha=0.7
)
plt.title(f"KMeans Clusters Visualization (n_clusters={n_clusters})")
plt.tight_layout()
plt.savefig(os.path.join(results_folder, "KMeans_PCA_Visualization.png"))
plt.close()

# =====================
# CLUSTER SIZE / DISTRIBUTION
# =====================
cluster_counts = df['cluster'].value_counts().sort_index()
cluster_counts.to_csv(os.path.join(results_folder, "KMeans_Cluster_Counts.csv"), header=['count'])
print(f"Cluster counts saved to: {results_folder}/KMeans_Cluster_Counts.csv")

print("Model 5 (Expense Structure Clustering) fixed & completed successfully!")
