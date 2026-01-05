import pandas as pd
import numpy as np
import os

# =========================
# CONFIG
# =========================

BASE_DIR = "/Users/anandhytapratamaputrisutisna/FYP2/Dataset2"

model3_path = "/Users/anandhytapratamaputrisutisna/FYP2/Data/dataset2_model3_results/Budget_Forecasting_Predictions.csv"
model4_path = "/Users/anandhytapratamaputrisutisna/FYP2/Data/dataset2_model4_results/Dataset2_Anomalies.csv"
model5_path = "/Users/anandhytapratamaputrisutisna/FYP2/Data/dataset2_model5_results/dataset2_clustered.csv"

OUTPUT_DIR = f"{BASE_DIR}/dataset2_financial_health"
OUTPUT_PATH = f"{OUTPUT_DIR}/financial_health.csv"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================
# LOAD DATA
# =========================

df_m3 = pd.read_csv(model3_path)
df_m4 = pd.read_csv(model4_path)
df_m5 = pd.read_csv(model5_path)

print("===== DATA LOADED =====")
print("Model 3:", df_m3.shape)
print("Model 4:", df_m4.shape)
print("Model 5:", df_m5.shape)

# =========================
# MERGE (LEFT & SAFE)
# =========================

df = df_m3.merge(df_m4, on="ID", how="left")
df = df.merge(df_m5[["ID", "cluster"]], on="ID", how="left")

# =========================
# CALCULATE RATIOS
# =========================

# Savings rate
if "savings_rate" not in df.columns:
    if all(col in df.columns for col in ["Income (USD)", "Expense (USD)"]):
        df["savings_rate"] = (
            (df["Income (USD)"] - df["Expense (USD)"])
            / (df["Income (USD)"] + 1e-6)
        )
    else:
        df["savings_rate"] = np.nan

# Expense to income ratio
if "expense_to_income_ratio" not in df.columns:
    if all(col in df.columns for col in ["Expense (USD)", "Income (USD)"]):
        df["expense_to_income_ratio"] = (
            df["Expense (USD)"] / (df["Income (USD)"] + 1e-6)
        )
    else:
        df["expense_to_income_ratio"] = np.nan

# Discretionary vs fixed ratio
if "discretionary_vs_fixed_ratio" not in df.columns:
    if all(col in df.columns for col in ["Discretionary (USD)", "Fixed (USD)"]):
        df["discretionary_vs_fixed_ratio"] = (
            df["Discretionary (USD)"] / (df["Fixed (USD)"] + 1e-6)
        )
    else:
        df["discretionary_vs_fixed_ratio"] = np.nan

# =========================
# NORMALIZE ANOMALY
# =========================
# Isolation Forest: -1 = anomaly, 1 = normal
if "anomaly" in df.columns:
    df["anomaly"] = df["anomaly"].map({-1: 1, 1: 0})
else:
    df["anomaly"] = np.nan

# =========================
# FINANCIAL HEALTH DECISION LAYER
# =========================

def evaluate_health(row):
    if (
        pd.isna(row.get("savings_rate"))
        and pd.isna(row.get("expense_to_income_ratio"))
        and pd.isna(row.get("discretionary_vs_fixed_ratio"))
    ):
        return pd.Series([
            "Moderate",
            0,
            "Insufficient financial indicators for full assessment"
        ])

    score = 0
    reasons = []

    # Savings behavior
    if pd.notna(row.get("savings_rate")):
        if row["savings_rate"] >= 0.2:
            score += 2
            reasons.append("Healthy savings rate")
        elif row["savings_rate"] >= 0.1:
            score += 1
            reasons.append("Moderate savings rate")
        else:
            reasons.append("Low savings rate")

    # Spending pressure
    if pd.notna(row.get("expense_to_income_ratio")):
        if row["expense_to_income_ratio"] < 0.6:
            score += 2
            reasons.append("Controlled spending")
        elif row["expense_to_income_ratio"] < 0.8:
            score += 1
            reasons.append("Moderate spending")
        else:
            reasons.append("High spending pressure")

    # Discretionary spending
    if pd.notna(row.get("discretionary_vs_fixed_ratio")):
        if row["discretionary_vs_fixed_ratio"] < 0.5:
            score += 1
            reasons.append("Balanced discretionary spending")
        else:
            reasons.append("High discretionary spending")

    # Anomaly penalty
    if row.get("anomaly") == 1:
        score -= 2
        reasons.append("Anomalous financial behavior detected")

    # Final label
    if score >= 4:
        label = "Healthy"
    elif score >= 2:
        label = "Moderate"
    else:
        label = "At Risk"

    return pd.Series([label, score, "; ".join(reasons)])

# =========================
# APPLY DECISION LAYER
# =========================

df[["financial_health", "health_score", "health_justification"]] = (
    df.apply(evaluate_health, axis=1)
)

# =========================
# FINANCIAL RISK LEVEL (NEW)
# =========================

df["financial_risk_level"] = df["financial_health"].map({
    "Healthy": "Low",
    "Moderate": "Medium",
    "At Risk": "High"
})

# =========================
# FINALIZE CSV
# =========================

final_cols = [
    "ID",
    "savings_rate",
    "expense_to_income_ratio",
    "discretionary_vs_fixed_ratio",
    "cluster",
    "anomaly",
    "financial_health",
    "financial_risk_level",   # 👈 NEW
    "health_score",
    "health_justification"
]

df_final = df[final_cols]
df_final.to_csv(OUTPUT_PATH, index=False)

print("===== FINANCIAL HEALTH PIPELINE COMPLETE =====")
print("Output saved to:", OUTPUT_PATH)
print("Shape:", df_final.shape)
