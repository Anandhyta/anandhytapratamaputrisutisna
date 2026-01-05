# =========================================
# behavior_insight.py
# Purpose:
#   Derive final user behavioral insight
#   by integrating:
#     - KMeans clustering (spending intensity)
#     - Isolation Forest (behavioral anomaly)
#
# Dataset:
#   Dataset 1 (Behavioral Transactions)
#
# Output:
#   behavior_insight/behavior_insight.csv
# =========================================

import pandas as pd
import os

# ===============================
# CONFIGURATION
# ===============================
MODEL1_FILE = "/Users/anandhytapratamaputrisutisna/FYP2/data/dataset1_model1_results/k3_interpretability/dataset1_kmeans.csv"
MODEL2_FILE = "/Users/anandhytapratamaputrisutisna/FYP2/data/dataset1_model2_results/automatic_contamination/dataset1_isolation_forest.csv"

OUTPUT_DIR = "/Users/anandhytapratamaputrisutisna/FYP2/data/behavior_insight"
os.makedirs(OUTPUT_DIR, exist_ok=True)

OUTPUT_FILE = os.path.join(OUTPUT_DIR, "behavior_insight.csv")

# ===============================
# LOAD MODEL OUTPUTS
# ===============================
kmeans_df = pd.read_csv(MODEL1_FILE)
iso_df = pd.read_csv(MODEL2_FILE)

# ===============================
# SELECT RELEVANT COLUMNS
# ===============================
kmeans_sel = kmeans_df[
    ["client_id", "time_window", "cluster_label"]
].rename(columns={"cluster_label": "spending_intensity"})

iso_sel = iso_df[
    ["client_id", "time_window", "anomaly_label"]
]

# ===============================
# MERGE MODEL RESULTS
# ===============================
merged = pd.merge(
    kmeans_sel,
    iso_sel,
    on=["client_id", "time_window"],
    how="inner"
)

# ===============================
# AGGREGATE AT USER LEVEL
# ===============================
user_agg = merged.groupby("client_id").agg(
    dominant_spending_intensity=(
        "spending_intensity",
        lambda x: x.value_counts().idxmax()
    ),
    anomaly_ratio=(
        "anomaly_label",
        lambda x: (x == "Anomaly").mean()
    )
).reset_index()

# ===============================
# DERIVED FLAGS
# ===============================
# Anomalies are rare; presence is more meaningful than frequency
user_agg["has_anomaly"] = user_agg["anomaly_ratio"] > 0

# ===============================
# FINAL BEHAVIOR CLASSIFICATION
# ===============================
def derive_behavior(row):
    """
    Behavioral interpretation logic:
    - Any detected anomaly → Inconsistent behavior
    - High dominant spending → Impulsive behavior
    - Otherwise → Stable behavior
    """
    if row["has_anomaly"]:
        return "Inconsistent"
    elif row["dominant_spending_intensity"] == "High":
        return "Impulsive"
    else:
        return "Stable"

user_agg["behavior_type"] = user_agg.apply(derive_behavior, axis=1)

# ===============================
# BEHAVIOR RISK LEVEL
# ===============================
risk_mapping = {
    "Stable": "Low",
    "Impulsive": "Medium",
    "Inconsistent": "High"
}
user_agg["behavior_risk_level"] = user_agg["behavior_type"].map(risk_mapping)

# ===============================
# JUSTIFICATION (FOR UI & EXPLAINABILITY)
# ===============================
user_agg["behavior_justification"] = (
    "Dominant intensity=" + user_agg["dominant_spending_intensity"]
    + ", anomaly_ratio=" + user_agg["anomaly_ratio"].round(2).astype(str)
)

# ===============================
# SAVE FINAL INSIGHT
# ===============================
user_agg.to_csv(OUTPUT_FILE, index=False)

print(f"Behavior insight saved to: {OUTPUT_FILE}")
print(user_agg.head())
