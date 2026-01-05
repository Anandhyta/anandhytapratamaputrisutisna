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
# FUNCTION: GET USER INSIGHT (Returns Dictionary for API)
# ===============================
def get_user_insight(user_id):
    """
    Get comprehensive user insight including behavior, financial health,
    expenses, recommendations, and insight text.
    
    Returns:
        dict: Contains all user insight data for API consumption
              - behavior_insight: dict with type, risk_level, details
              - financial_insight: dict with health, score, risk_level, details
              - current_expenses: dict of expense categories
              - recommended_expenses: dict of recommended amounts
              - income: float
              - total_expenses: float
              - insight_text: str
        None: If user not found
    """
    # Get user rows from datasets
    behavior_row = df_behavior[df_behavior["client_id"] == user_id]
    financial_row = df_financial[df_financial["ID"] == user_id]

    if behavior_row.empty and financial_row.empty:
        return None  # User not found

    behavior_data = behavior_row.iloc[0] if not behavior_row.empty else None
    financial_data = financial_row.iloc[0] if not financial_row.empty else None

    # Generate recommendation using existing function
    rec = generate_financial_recommendation(user_id, behavior_data, financial_data)

    # ===============================
    # BUILD BEHAVIOR INSIGHT DICT
    # ===============================
    behavior_insight = {
        "behavior_type": behavior_data["behavior_type"] if behavior_data is not None else "Unknown",
        "behavior_risk_level": behavior_data["behavior_risk_level"] if behavior_data is not None else "Unknown",
        "behavior_details": behavior_data["behavior_justification"] if behavior_data is not None else "No behavior data available"
    }

    # ===============================
    # BUILD FINANCIAL INSIGHT DICT
    # ===============================
    financial_insight = {
        "financial_health": financial_data["financial_health"] if financial_data is not None else "Unknown",
        "health_score": float(financial_data["health_score"]) if financial_data is not None else 0.0,
        "financial_risk_level": financial_data["financial_risk_level"] if financial_data is not None else "Unknown",
        "financial_details": financial_data["health_justification"] if financial_data is not None else "No financial data available"
    }

    # ===============================
    # RETURN COMPLETE INSIGHT DICTIONARY
    # ===============================
    return {
        "behavior_insight": behavior_insight,
        "financial_insight": financial_insight,
        "current_expenses": rec.get("current_expenses"),
        "recommended_expenses": rec.get("recommended_expenses"),
        "income": rec.get("income"),
        "total_expenses": rec.get("total_expenses"),
        "insight_text": rec.get("insight_text", "")
    }


# ===============================
# FUNCTION: GET USER INSIGHT AS TEXT (For CLI/Debug)
# ===============================
def get_user_insight_text(user_id):
    """
    Get user insight as formatted text string (for CLI usage).
    """
    data = get_user_insight(user_id)
    
    if data is None:
        return f"No data available for User ID: {user_id}"

    output = f"User ID: {user_id}\n\n"

    # Current Expenses
    if data["current_expenses"]:
        output += "Current Expenses:\n"
        for k, v in data["current_expenses"].items():
            output += f"  - {k}: {v:.2f} USD\n"
        output += "\n"

    # Behavior Insight
    output += "Behavior Insight:\n"
    output += f"  Type: {data['behavior_insight']['behavior_type']}\n"
    output += f"  Risk Level: {data['behavior_insight']['behavior_risk_level']}\n"
    output += f"  Details: {data['behavior_insight']['behavior_details']}\n\n"

    # Financial Insight
    output += "Financial Insight:\n"
    output += f"  Health: {data['financial_insight']['financial_health']}\n"
    output += f"  Risk Level: {data['financial_insight']['financial_risk_level']}\n"
    output += f"  Score: {data['financial_insight']['health_score']}\n"
    output += f"  Details: {data['financial_insight']['financial_details']}\n\n"

    # Recommended Budget
    if data["recommended_expenses"]:
        output += "Recommended Budget for Next Month:\n"
        for k, v in data["recommended_expenses"].items():
            output += f"  - {k}: {v:.2f} USD\n"
        output += "\n"

    # Insight Text
    output += "Recommendation Insight Text:\n"
    output += data["insight_text"]

    return output

# ===============================
# EXAMPLE USAGE
# ===============================
if __name__ == "__main__":
    try:
        user_id_input = int(input("Enter User ID: "))
        result = get_user_insight_text(user_id_input)
        print("\n" + result)
    except ValueError:
        print("Invalid input. Please enter a numeric User ID.")
