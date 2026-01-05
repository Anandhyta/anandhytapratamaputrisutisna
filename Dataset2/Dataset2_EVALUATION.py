import pandas as pd
import os
import numpy as np
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.metrics import silhouette_score

# =====================
# PATHS
# =====================
model3_results = "/Users/anandhytapratamaputrisutisna/FYP2/Data/dataset2_model3_results"
model4_results = "/Users/anandhytapratamaputrisutisna/FYP2/Data/dataset2_model4_results"
model5_results = "/Users/anandhytapratamaputrisutisna/FYP2/Data/dataset2_model5_results"
evaluation_folder = "/Users/anandhytapratamaputrisutisna/FYP2/Data/dataset2_evaluation"
os.makedirs(evaluation_folder, exist_ok=True)

# =====================
# LOAD MODEL RESULTS
# =====================

# Model 3: Budget Forecasting
pred_file = os.path.join(model3_results, "Budget_Forecasting_Predictions.csv")
rf_feature_file = os.path.join(model3_results, "RandomForest_Feature_Importance.csv")
vis_actual_vs_pred = os.path.join(model3_results, "Actual_vs_Predicted.png")
vis_feature_importance = os.path.join(model3_results, "Feature_Importance.png")

predictions_df = pd.read_csv(pred_file) if os.path.exists(pred_file) else None
rf_feature_importance = pd.read_csv(rf_feature_file) if os.path.exists(rf_feature_file) else None

# Model 4: Overspending / Anomaly Detection
anomaly_file = os.path.join(model4_results, "IsolationForest_Evaluation.csv")
model4_summary = pd.read_csv(anomaly_file) if os.path.exists(anomaly_file) else None

# Model 5: Expense Clustering
kmeans_summary_file = os.path.join(model5_results, "KMeans_Cluster_Summary.csv")
kmeans_counts_file = os.path.join(model5_results, "KMeans_Cluster_Counts.csv")
clustered_data_file = os.path.join(model5_results, "dataset2_clustered.csv") 
kmeans_summary = pd.read_csv(kmeans_summary_file) if os.path.exists(kmeans_summary_file) else None
kmeans_counts = pd.read_csv(kmeans_counts_file) if os.path.exists(kmeans_counts_file) else None
clustered_df = pd.read_csv(clustered_data_file) if os.path.exists(clustered_data_file) else None

# =====================
# EVALUATION SUMMARY
# =====================
summary_text_file = os.path.join(evaluation_folder, "Dataset2_Evaluation_Summary.txt")
with open(summary_text_file, "w") as f:
    f.write("===== DATASET2 EVALUATION SUMMARY =====\n\n")

    # ---------------------
    # Model 3: Budget Forecasting
    # ---------------------
    f.write(">> MODEL 3: Budget Forecasting\n")
    if rf_feature_importance is not None:
        f.write("Top 5 features by importance (Random Forest):\n")
        f.write(rf_feature_importance.head().to_string(index=False))
        f.write("\n")
    
    if predictions_df is not None:
        f.write("Sample predictions (first 5 rows):\n")
        f.write(predictions_df.head().to_string(index=False))
        f.write("\n")
        
        # Metrics
        y_true = predictions_df['Actual']
        y_pred_linear = predictions_df['Pred_Linear']
        y_pred_rf = predictions_df['Pred_RF']

        r2_linear = r2_score(y_true, y_pred_linear)
        mae_linear = mean_absolute_error(y_true, y_pred_linear)
        rmse_linear = np.sqrt(mean_squared_error(y_true, y_pred_linear))

        r2_rf = r2_score(y_true, y_pred_rf)
        mae_rf = mean_absolute_error(y_true, y_pred_rf)
        rmse_rf = np.sqrt(mean_squared_error(y_true, y_pred_rf))

        f.write("Regression Metrics:\n")
        f.write(f"Linear Regression -> R²: {r2_linear:.4f}, RMSE: {rmse_linear:.2f}, MAE: {mae_linear:.2f}\n")
        f.write(f"Random Forest     -> R²: {r2_rf:.4f}, RMSE: {rmse_rf:.2f}, MAE: {mae_rf:.2f}\n")

        best_model_3 = "Linear Regression" if r2_linear > r2_rf else "Random Forest"
        f.write(f"Best model based on evaluation: {best_model_3}\n\n")
    
    f.write("Visualizations (check saved images):\n")
    f.write(f"- Actual vs Predicted: {vis_actual_vs_pred}\n")
    f.write(f"- Feature Importance: {vis_feature_importance}\n\n")

    # ---------------------
    # Model 4: Overspending / Anomaly Detection
    # ---------------------
    f.write(">> MODEL 4: Overspending / Anomaly Detection\n")
    if model4_summary is not None and not model4_summary.empty:
        total_anomalies = len(model4_summary['Sample Client IDs'].values[0].strip('[]').split(','))
        f.write(f"Percentage of anomalies: {model4_summary['% Anomaly'].values[0]:.2f}%\n")
        f.write(f"Sample anomaly client IDs: {model4_summary['Sample Client IDs'].values[0]}\n")
        f.write("Recommended model: Isolation Forest (based on anomaly coverage)\n\n")
    else:
        f.write("No anomaly data found or file is empty.\n\n")

    # ---------------------
    # Model 5: Expense Structure Clustering
    # ---------------------
    f.write(">> MODEL 5: Expense Structure Clustering\n")
    if kmeans_counts is not None:
        f.write("Cluster Counts:\n")
        f.write(kmeans_counts.to_string(index=False))
        f.write("\n")
    
    if clustered_df is not None and 'cluster' in clustered_df.columns:
        try:
            X = clustered_df.drop(columns=['cluster']).values
            cluster_labels = clustered_df['cluster'].values
            sil_score = silhouette_score(X, cluster_labels)
            f.write(f"Silhouette Score: {sil_score:.4f}\n")
            f.write("Representative cluster centroids (cluster means):\n")
            f.write(kmeans_summary.to_string(index=False))
            f.write(f"\nRecommended n_clusters based on silhouette score: {len(kmeans_counts)}\n\n")
        except Exception as e:
            f.write(f"Silhouette score calculation skipped (error: {e})\n\n")
    else:
        f.write("Silhouette score calculation skipped (dataset with cluster labels not found)\n\n")

print(f"Evaluation summary saved to: {summary_text_file}")
print("Evaluation complete. Output saved to Dataset2_Evaluation_Summary.txt")
