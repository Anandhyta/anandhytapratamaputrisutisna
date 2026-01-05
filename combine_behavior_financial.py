# ========================================
# combine_behavior_financial_full.py
# Purpose:
#   Combine behavior insight (Dataset 1)
#   + financial insight (Dataset 2)
#   based on all unique IDs from both datasets
# ========================================

import pandas as pd
import os

# =========================
# CONFIG
# =========================
BEHAVIOR_FILE = "/Users/anandhytapratamaputrisutisna/FYP2/data/behavior_insight/behavior_insight.csv"
FINANCIAL_FILE = "/Users/anandhytapratamaputrisutisna/FYP2/Dataset2/dataset2_financial_health/financial_health.csv"

OUTPUT_DIR = "/Users/anandhytapratamaputrisutisna/FYP2/Dataset2/dataset2_combined_insight"
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_FILE = f"{OUTPUT_DIR}/combined_insight.csv"

# =========================
# LOAD DATA
# =========================
df_behavior = pd.read_csv(BEHAVIOR_FILE)
df_financial = pd.read_csv(FINANCIAL_FILE)

print("Behavior Insight:", df_behavior.shape)
print("Financial Insight:", df_financial.shape)

# =========================
# CREATE FULL ID LIST
# =========================
all_ids = pd.Series(
    sorted(set(df_behavior['client_id']) | set(df_financial['ID'])), 
    name='ID'
)
df_all = pd.DataFrame(all_ids)

# =========================
# MERGE BEHAVIOR
# =========================
df_all = df_all.merge(df_behavior, left_on='ID', right_on='client_id', how='left')
df_all.drop(columns=['client_id'], inplace=True)

# =========================
# MERGE FINANCIAL
# =========================
df_all = df_all.merge(df_financial, on='ID', how='left')

# =========================
# FILL MISSING VALUES / DEFAULTS
# =========================
# Behavior defaults
df_all['dominant_spending_intensity'] = df_all['dominant_spending_intensity'].fillna('Unknown')
df_all['anomaly_ratio'] = df_all['anomaly_ratio'].fillna(0)
df_all['has_anomaly'] = df_all['has_anomaly'].fillna(False)
df_all['behavior_type'] = df_all['behavior_type'].fillna('Unknown')
df_all['behavior_risk_level'] = df_all['behavior_risk_level'].fillna('Unknown')
df_all['behavior_justification'] = df_all['behavior_justification'].fillna('')

# Financial defaults
df_all['savings_rate'] = df_all['savings_rate'].fillna(0)
df_all['expense_to_income_ratio'] = df_all['expense_to_income_ratio'].fillna(0)
df_all['discretionary_vs_fixed_ratio'] = df_all['discretionary_vs_fixed_ratio'].fillna(0)
df_all['cluster'] = df_all['cluster'].fillna(-1)
df_all['anomaly'] = df_all['anomaly'].fillna(0)
df_all['financial_health'] = df_all['financial_health'].fillna('Unknown')
df_all['health_score'] = df_all['health_score'].fillna(0)
df_all['health_justification'] = df_all['health_justification'].fillna('')

# =========================
# SAVE CSV
# =========================
df_all.to_csv(OUTPUT_FILE, index=False)
print("Combined insight saved to:", OUTPUT_FILE)
print("Shape:", df_all.shape)
print(df_all.head())
