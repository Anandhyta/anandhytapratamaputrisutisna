# =========================================
# get_user_insight.py
# Purpose:
#   Combine behavior insight, financial insight, insight_text, recommendation
#   for a single user
# =========================================

import pandas as pd
from recommendation import generate_financial_recommendation

# ===============================
# CONFIG
# ===============================
BEHAVIOR_FILE = "/Users/anandhytapratamaputrisutisna/FYP2/data/behavior_insight/behavior_insight.csv"
FINANCIAL_FILE = "/Users/anandhytapratamaputrisutisna/FYP2/Dataset2/dataset2_financial_health/financial_health.csv"
# ===============================
# LOAD INSIGHTS
# ===============================
df_behavior = pd.read_csv(BEHAVIOR_FILE)
df_financial = pd.read_csv(FINANCIAL_FILE)

# ===============================
# FUNCTION: GET USER INSIGHT
# ===============================
def get_user_insight(user_id):
    # Ambil baris user
    behavior_row = df_behavior[df_behavior["client_id"] == user_id]
    financial_row = df_financial[df_financial["ID"] == user_id]

    if behavior_row.empty and financial_row.empty:
        return f"No data available for User ID: {user_id}"

    behavior_row = behavior_row.iloc[0] if not behavior_row.empty else None
    financial_row = financial_row.iloc[0] if not financial_row.empty else None

    # Generate recommendation
    rec = generate_financial_recommendation(user_id, behavior_row, financial_row)

    # Format output untuk UI
    output = f"User ID: {user_id}\n\n"

    # ===============================
    # CURRENT EXPENSES
    # ===============================
    if rec["current_expenses"]:
        output += "Current Expenses:\n"
        for k,v in rec["current_expenses"].items():
            output += f"  - {k}: {v:.2f} USD\n"
        output += "\n"

    # ===============================
    # BEHAVIOR INSIGHT
    # ===============================
    if behavior_row is not None:
        output += "Behavior Insight:\n"
        output += f"  Type: {behavior_row['behavior_type']}\n"
        output += f"  Risk Level: {behavior_row['behavior_risk_level']}\n"
        output += f"  Details: {behavior_row['behavior_justification']}\n\n"

    # ===============================
    # FINANCIAL INSIGHT
    # ===============================
    if financial_row is not None:
        output += "Financial Insight:\n"
        output += f"  Health: {financial_row['financial_health']}\n"
        output += f"  Risk Level: {financial_row['financial_risk_level']}\n"
        output += f"  Score: {financial_row['health_score']}\n"
        output += f"  Details: {financial_row['health_justification']}\n\n"

    # ===============================
    # RECOMMENDED BUDGET
    # ===============================
    if rec["recommended_expenses"]:
        output += "Recommended Budget for Next Month:\n"
        for k,v in rec["recommended_expenses"].items():
            output += f"  - {k}: {v:.2f} USD\n"
        output += "\n"

    # ===============================
    # RECOMMENDATION INSIGHT TEXT
    # ===============================
    output += "Recommendation Insight Text:\n"
    output += rec["insight_text"]

    return output

# ===============================
# EXAMPLE USAGE
# ===============================
if __name__ == "__main__":
    try:
        user_id_input = int(input("Enter User ID: "))
        result = get_user_insight(user_id_input)
        print("\n" + result)
    except ValueError:
        print("Invalid input. Please enter a numeric User ID.")
