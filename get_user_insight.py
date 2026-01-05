# =========================================
# get_user_insight.py
# Purpose:
#   Combine behavior insight, financial insight, insight_text, recommendation
#   for a single user
#   WITH real-time overspending detection
# =========================================

import pandas as pd
from recommendation import generate_financial_recommendation

# ===============================
# CONFIG
# ===============================
BEHAVIOR_FILE = "/Users/anandhytapratamaputrisutisna/FYP2/data/behavior_insight/behavior_insight.csv"
FINANCIAL_FILE = "/Users/anandhytapratamaputrisutisna/FYP2/Dataset2/dataset2_financial_health/financial_health.csv"
EXPENSES_FILE = "/Users/anandhytapratamaputrisutisna/FYP2/Data/dataset2_anomaly_results/Sample_Anomalous_Transactions.csv"

# ===============================
# LOAD INSIGHTS
# ===============================
df_behavior = pd.read_csv(BEHAVIOR_FILE)
df_financial = pd.read_csv(FINANCIAL_FILE)
df_expenses = pd.read_csv(EXPENSES_FILE)


# ===============================
# HELPER: Calculate Real Financial Health
# ===============================
def calculate_real_financial_health(user_id, income, total_expenses):
    """
    Calculate financial health based on ACTUAL income vs expenses.
    This overrides the pre-computed health if user is overspending.
    """
    if income is None or income == 0:
        return {
            "financial_health": "Unknown",
            "health_score": 0,
            "financial_risk_level": "Unknown",
            "financial_details": "Income data not available"
        }
    
    # Calculate expense to income ratio
    expense_ratio = total_expenses / income
    savings_rate = (income - total_expenses) / income
    
    score = 0
    reasons = []
    
    # Overspending check (CRITICAL - highest priority)
    if expense_ratio > 1.5:
        score -= 3
        reasons.append(f"CRITICAL overspending: spending {expense_ratio:.1f}x income")
    elif expense_ratio > 1.0:
        score -= 2
        overspend_pct = (expense_ratio - 1) * 100
        reasons.append(f"Overspending by {overspend_pct:.0f}% of income")
    elif expense_ratio > 0.9:
        score -= 1
        reasons.append("Living paycheck to paycheck (spending >90% of income)")
    elif expense_ratio > 0.8:
        score += 1
        reasons.append("Moderate spending (80-90% of income)")
    else:
        score += 2
        reasons.append(f"Healthy spending ({expense_ratio*100:.0f}% of income)")
    
    # Savings rate check
    if savings_rate >= 0.2:
        score += 2
        reasons.append(f"Excellent savings rate ({savings_rate*100:.0f}%)")
    elif savings_rate >= 0.1:
        score += 1
        reasons.append(f"Good savings rate ({savings_rate*100:.0f}%)")
    elif savings_rate >= 0:
        reasons.append(f"Low savings rate ({savings_rate*100:.0f}%)")
    else:
        score -= 1
        reasons.append(f"Negative savings (debt accumulation)")
    
    # Determine health level
    if score >= 3:
        health_level = "Healthy"
        risk_level = "Low"
    elif score >= 1:
        health_level = "Moderate"
        risk_level = "Medium"
    elif score >= -1:
        health_level = "At Risk"
        risk_level = "High"
    else:
        health_level = "Critical"
        risk_level = "Very High"
    
    return {
        "financial_health": health_level,
        "health_score": score,
        "financial_risk_level": risk_level,
        "financial_details": "; ".join(reasons)
    }


# ===============================
# HELPER: Calculate Real Behavior Risk
# ===============================
def calculate_real_behavior_risk(behavior_data, expense_ratio):
    """
    Adjust behavior risk based on actual overspending.
    Someone spending 2.5x their income is NOT "Low" risk!
    """
    if behavior_data is None:
        base_type = "Unknown"
        base_risk = "Unknown"
        base_details = "No behavior data available"
    else:
        base_type = behavior_data.get("behavior_type", "Unknown")
        base_risk = behavior_data.get("behavior_risk_level", "Unknown")
        base_details = behavior_data.get("behavior_justification", "")
    
    # Override risk if overspending detected
    adjusted_risk = base_risk
    adjusted_type = base_type
    additional_note = ""
    
    if expense_ratio is not None:
        if expense_ratio > 1.5:
            adjusted_risk = "Very High"
            if base_type == "Stable":
                adjusted_type = "Consistently Overspending"
            additional_note = f" | WARNING: Spending {expense_ratio:.1f}x income"
        elif expense_ratio > 1.0:
            if adjusted_risk == "Low":
                adjusted_risk = "High"
            elif adjusted_risk == "Medium":
                adjusted_risk = "High"
            additional_note = f" | Overspending detected"
    
    return {
        "behavior_type": adjusted_type,
        "behavior_risk_level": adjusted_risk,
        "behavior_details": base_details + additional_note
    }


# ===============================
# FUNCTION: GET USER INSIGHT (Returns Dictionary for API)
# ===============================
def get_user_insight(user_id):
    """
    Get comprehensive user insight including behavior, financial health,
    expenses, recommendations, and insight text.
    
    Now includes REAL-TIME overspending detection!
    """
    # Get user rows from datasets
    behavior_row = df_behavior[df_behavior["client_id"] == user_id]
    financial_row = df_financial[df_financial["ID"] == user_id]
    expenses_row = df_expenses[df_expenses["ID"] == user_id]

    if behavior_row.empty and financial_row.empty and expenses_row.empty:
        return None  # User not found

    behavior_data = behavior_row.iloc[0].to_dict() if not behavior_row.empty else None
    financial_data = financial_row.iloc[0].to_dict() if not financial_row.empty else None

    # Generate recommendation using existing function
    rec = generate_financial_recommendation(user_id, behavior_data, financial_data)

    # Get actual income and expenses
    income = rec.get("income")
    total_expenses = rec.get("total_expenses")
    
    # Calculate expense ratio for risk adjustment
    expense_ratio = total_expenses / income if income and income > 0 else None

    # ===============================
    # BUILD FINANCIAL INSIGHT (REAL-TIME CALCULATION)
    # ===============================
    if income and total_expenses:
        # Use real-time calculation based on actual data
        financial_insight = calculate_real_financial_health(user_id, income, total_expenses)
    elif financial_data is not None:
        # Fallback to pre-computed data
        financial_insight = {
            "financial_health": financial_data.get("financial_health", "Unknown"),
            "health_score": float(financial_data.get("health_score", 0)),
            "financial_risk_level": financial_data.get("financial_risk_level", "Unknown"),
            "financial_details": financial_data.get("health_justification", "No financial data available")
        }
    else:
        financial_insight = {
            "financial_health": "Unknown",
            "health_score": 0,
            "financial_risk_level": "Unknown",
            "financial_details": "No financial data available"
        }

    # ===============================
    # BUILD BEHAVIOR INSIGHT (WITH OVERSPENDING ADJUSTMENT)
    # ===============================
    behavior_insight = calculate_real_behavior_risk(behavior_data, expense_ratio)

    # ===============================
    # RETURN COMPLETE INSIGHT DICTIONARY
    # ===============================
    return {
        "behavior_insight": behavior_insight,
        "financial_insight": financial_insight,
        "current_expenses": rec.get("current_expenses"),
        "recommended_expenses": rec.get("recommended_expenses"),
        "income": income,
        "total_expenses": total_expenses,
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
