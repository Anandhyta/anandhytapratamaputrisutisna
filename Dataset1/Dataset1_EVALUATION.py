import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
from sklearn.metrics import silhouette_score, davies_bouldin_score
from sklearn.decomposition import PCA
import plotly.express as px

# =====================
# FOLDER STRUCTURE
# =====================
evaluation_folder = "/Users/anandhytapratamaputrisutisna/FYP2/Data/dataset1_evaluation"
os.makedirs(evaluation_folder, exist_ok=True)

# =====================
# LOAD DATA
# =====================
summary_file = "/Users/anandhytapratamaputrisutisna/FYP2/Data/dataset1_summary.csv"
transactions_file = "/Users/anandhytapratamaputrisutisna/FYP2/Data/dataset1_transactions.csv"

df_summary = pd.read_csv(summary_file)
df_trans = pd.read_csv(transactions_file)

# =====================
# FEATURES & SCALING
# =====================
numerical_cols = ['total_spending', 'transaction_count', 'avg_transaction_value',
                  'spending_variance', 'max_amount', 'min_amount', 'weekend_spending_ratio']
X = df_summary[numerical_cols]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# =====================
# MODEL 1: Expense Structure Clustering (KMeans)
# =====================
k = 3
kmeans = KMeans(n_clusters=k, random_state=42)
df_summary['cluster'] = kmeans.fit_predict(X_scaled)

silhouette = silhouette_score(X_scaled, df_summary['cluster'])
db_index = davies_bouldin_score(X_scaled, df_summary['cluster'])
cluster_counts = df_summary['cluster'].value_counts().sort_index()

# =====================
# MODEL 2: Overspending / Anomaly Detection (Isolation Forest)
# =====================
iso = IsolationForest(contamination='auto', random_state=42)
df_summary['anomaly'] = iso.fit_predict(X_scaled)  # -1 = anomaly
num_anomalies = (df_summary['anomaly'] == -1).sum()
percent_anomalies = num_anomalies / len(df_summary) * 100
sample_anomaly_ids = df_summary[df_summary['anomaly']==-1]['client_id'].tolist()[:5]

df_anomaly_trans = df_trans[df_trans['client_id'].isin(sample_anomaly_ids)]
anomaly_trans_file = os.path.join(evaluation_folder, 'Sample_Anomalous_Transactions.csv')
df_anomaly_trans.to_csv(anomaly_trans_file, index=False)

# =====================
# PCA VISUALIZATION
# =====================
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
df_summary['PCA1'] = X_pca[:,0]
df_summary['PCA2'] = X_pca[:,1]

# Static plot
plt.figure(figsize=(8,6))
palette = sns.color_palette("Set2", k)
sns.scatterplot(
    data=df_summary,
    x='PCA1', y='PCA2',
    hue='cluster', palette=palette,
    style=df_summary['anomaly'].map({1:'Normal', -1:'Anomaly'}),
    size=df_summary['anomaly'].map({1:50, -1:200}),
    alpha=0.7
)
plt.title(f'KMeans (k={k}) Clusters with Isolation Forest Anomalies')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.legend(title='Cluster / Anomaly', bbox_to_anchor=(1.05,1), loc='upper left')
plt.tight_layout()
static_plot_file = os.path.join(evaluation_folder, 'KMeans_IsolationForest_PCA_Static.png')
plt.savefig(static_plot_file)
plt.close()

# Interactive plot
df_summary['anomaly_label'] = df_summary['anomaly'].map({1:'Normal', -1:'Anomaly'})
df_summary['hover_text'] = df_summary.apply(
    lambda row: f"Client ID: {row['client_id']}<br>"
                f"Cluster: {row['cluster']}<br>"
                f"Anomaly: {row['anomaly_label']}<br>"
                f"Total Spending: {row['total_spending']:.2f}",
    axis=1
)
import plotly.express as px
fig = px.scatter(
    df_summary,
    x='PCA1',
    y='PCA2',
    color='cluster',
    symbol='anomaly_label',
    size=df_summary['anomaly'].map({1:5, -1:10}),
    hover_name='hover_text',
    title=f'KMeans (k={k}) Clusters with Isolation Forest Anomalies'
)
fig.update_layout(legend_title_text='Cluster / Anomaly', width=900, height=700)
interactive_file = os.path.join(evaluation_folder, 'KMeans_IsolationForest_PCA_Interactive.html')
fig.write_html(interactive_file)

# =====================
# PRINT & SAVE EVALUATION SUMMARY
# =====================
summary_txt = os.path.join(evaluation_folder, 'Dataset1_Evaluation_Summary.txt')
with open(summary_txt, 'w') as f:
    f.write("===== DATASET1 EVALUATION SUMMARY =====\n\n")
    
    f.write(">> MODEL 1: Expense Structure Clustering (KMeans)\n")
    f.write("Cluster Counts:\n")
    f.write(cluster_counts.to_string())
    f.write(f"\nSilhouette Score: {silhouette:.4f}\n")
    f.write(f"Davies-Bouldin Index: {db_index:.4f}\n")
    f.write(f"Interpretability: {k} clusters\n\n")
    
    f.write(">> MODEL 2: Overspending / Anomaly Detection (Isolation Forest)\n")
    f.write(f"Total anomalies detected: {num_anomalies}\n")
    f.write(f"Percentage of anomalies: {percent_anomalies:.2f}%\n")
    f.write(f"Sample anomaly client IDs: {sample_anomaly_ids}\n\n")
    
    f.write(f"Sample anomalous transactions saved to: {anomaly_trans_file}\n")
    f.write(f"Static PCA plot saved to: {static_plot_file}\n")
    f.write(f"Interactive PCA plot saved to: {interactive_file}\n")

print(f"Evaluation summary saved to: {summary_txt}")
print("Evaluation complete. Output saved to Dataset1_Evaluation_Summary.txt")
