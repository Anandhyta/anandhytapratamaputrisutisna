# # =========================================
# # recommendation.py (Realistic % Change Version)
# # Purpose:
# #   Generate monthly financial recommendation based on:
# #     - User expenses breakdown (Dataset 2)
# #     - Behavior insight
# #     - Financial insight
# #   Combines health-based rules + 50/30/20 allocation
# #   Provides human-readable, explanatory insights with capped changes
# # =========================================

# import pandas as pd
# import numpy as np

# # ===============================
# # CONFIGURATION
# # ===============================
# DATASET2_FILE = "/Users/anandhytapratamaputrisutisna/FYP2/Data/dataset2_anomaly_results/Sample_Anomalous_Transactions.csv"
# MAX_CHANGE_PERCENT = 0.25  # maximum 25% change per category

# # ===============================
# # LOAD DATA
# # ===============================
# df_expenses = pd.read_csv(DATASET2_FILE)

# # ===============================
# # FUNCTION: GENERATE FINANCIAL RECOMMENDATION
# # ===============================
# def generate_financial_recommendation(user_id, behavior_row=None, financial_row=None):
#     # -------------------------------
#     # Get user expense data
#     # -------------------------------
#     user_exp = df_expenses[df_expenses["ID"] == user_id]

#     if user_exp.empty:
#         return {
#             "current_expenses": None,
#             "recommended_expenses": None,
#             "insight_text": "No expense data available for this user."
#         }

#     expense_cols = [
#         "Rent (USD)", "Groceries (USD)", "Eating Out (USD)", "Entertainment (USD)",
#         "Subscription Services (USD)", "Education (USD)", "Online Shopping (USD)",
#         "Savings (USD)", "Investments (USD)", "Travel (USD)", "Fitness (USD)", "Miscellaneous (USD)"
#     ]

#     current_expenses = user_exp[expense_cols].iloc[0].to_dict()
#     total_expenses = sum(current_expenses.values())
#     recommended_expenses = current_expenses.copy()

#     # -------------------------------
#     # Financial health rules
#     # -------------------------------
#     health_level = financial_row.get("financial_health") if financial_row is not None else "Moderate"

#     if health_level == "Healthy":
#         recommended_expenses["Savings (USD)"] += 0.05 * total_expenses
#         recommended_expenses["Investments (USD)"] += 0.05 * total_expenses
#     elif health_level == "Moderate":
#         for col in ["Eating Out (USD)", "Entertainment (USD)", "Online Shopping (USD)"]:
#             recommended_expenses[col] *= 0.7
#         recommended_expenses["Savings (USD)"] += 0.05 * total_expenses
#     else:  # At Risk
#         for col in ["Eating Out (USD)", "Entertainment (USD)", "Online Shopping (USD)", "Travel (USD)"]:
#             recommended_expenses[col] *= 0.5
#         recommended_expenses["Savings (USD)"] += 0.1 * total_expenses

#     # -------------------------------
#     # 50/30/20 allocation
#     # -------------------------------
#     needs = ["Rent (USD)", "Groceries (USD)", "Education (USD)"]
#     wants = ["Eating Out (USD)", "Entertainment (USD)", "Online Shopping (USD)",
#              "Travel (USD)", "Subscription Services (USD)", "Fitness (USD)", "Miscellaneous (USD)"]
#     savings_investments = ["Savings (USD)", "Investments (USD)"]

#     total_income = total_expenses

#     needs_target = 0.5 * total_income
#     wants_target = 0.3 * total_income
#     savings_target = 0.2 * total_income

#     # Scale each category proportionally but capped at MAX_CHANGE_PERCENT
#     def apply_scaled_allocation(categories, target_sum):
#         current_sum = sum(recommended_expenses[c] for c in categories)
#         if current_sum == 0:
#             return
#         scale = target_sum / current_sum
#         for c in categories:
#             new_value = recommended_expenses[c] * scale
#             # Cap change to ±MAX_CHANGE_PERCENT
#             max_inc = recommended_expenses[c] * (1 + MAX_CHANGE_PERCENT)
#             max_dec = recommended_expenses[c] * (1 - MAX_CHANGE_PERCENT)
#             recommended_expenses[c] = min(max(max_dec, new_value), max_inc)

#     apply_scaled_allocation(needs, needs_target)
#     apply_scaled_allocation(wants, wants_target)
#     apply_scaled_allocation(savings_investments, savings_target)

#     # -------------------------------
#     # Human-readable insight text
#     # -------------------------------
#     behavior_type = behavior_row.get("behavior_type") if behavior_row is not None else "Unknown"
#     behavior_risk = behavior_row.get("behavior_risk_level") if behavior_row is not None else "Unknown"
#     financial_score = financial_row.get("health_score") if financial_row is not None else 0

#     insight_lines = [
#         f"Hello! Here's your personalized financial insight for next month:",
#         f"- Spending behavior: '{behavior_type}' (Risk Level: {behavior_risk})",
#         f"- Financial health: '{health_level}' (Score: {financial_score})",
#         "",
#         "Based on your current spending patterns and the 50/30/20 rule, we suggest the following adjustments:"
#     ]

#     for cat in expense_cols:
#         current = current_expenses.get(cat, 0)
#         recommended = recommended_expenses.get(cat, 0)
#         if abs(current - recommended) > 1e-2:
#             pct_change = (recommended - current) / (current + 1e-6) * 100 if current > 0 else 0
#             if recommended > current:
#                 reason = "increase savings or investment focus" if cat in savings_investments else "adjust proportion to match financial health targets"
#                 insight_lines.append(
#                     f"- {cat}: increase from {current:.2f} USD to {recommended:.2f} USD (+{pct_change:.1f}%) to {reason}."
#                 )
#             else:
#                 reason = "reduce discretionary spending" if cat in wants else "adjust proportion to match financial health targets"
#                 insight_lines.append(
#                     f"- {cat}: decrease from {current:.2f} USD to {recommended:.2f} USD ({pct_change:.1f}%) to {reason}."
#                 )

#     # Highlight high discretionary spending
#     for cat in wants:
#         ratio = current_expenses.get(cat,0) / (total_expenses + 1e-6)
#         if ratio > 0.2:
#             insight_lines.append(f"* Note: {cat} makes up more than 20% of your total expenses, consider moderating it.")

#     insight_lines.append("\nThese recommendations aim to help you balance your needs, wants, and savings while keeping financial health stable.")

#     insight_text = "\n".join(insight_lines)

#     return {
#         "current_expenses": current_expenses,
#         "recommended_expenses": recommended_expenses,
#         "insight_text": insight_text
#     }

# =========================================
# recommendation.py (With Income & Total Expenses)
# Purpose:
#   Generate monthly financial recommendation based on:
#     - User expenses breakdown (Dataset 2)
#     - Behavior insight
#     - Financial insight
#   Combines health-based rules + 50/30/20 allocation
#   Provides human-readable, explanatory insights with capped changes
# =========================================

import pandas as pd
import numpy as np

# ===============================
# CONFIGURATION
# ===============================
DATASET2_FILE = "/Users/anandhytapratamaputrisutisna/FYP2/Data/dataset2_anomaly_results/Sample_Anomalous_Transactions.csv"
MAX_CHANGE_PERCENT = 0.25  # maximum 25% change per category

# ===============================
# LOAD DATA
# ===============================
df_expenses = pd.read_csv(DATASET2_FILE)

# ===============================
# FUNCTION: GENERATE FINANCIAL RECOMMENDATION
# ===============================
def generate_financial_recommendation(user_id, behavior_row=None, financial_row=None):
    # -------------------------------
    # Get user expense data
    # -------------------------------
    user_exp = df_expenses[df_expenses["ID"] == user_id]

    if user_exp.empty:
        return {
            "current_expenses": None,
            "recommended_expenses": None,
            "income": None,
            "total_expenses": None,
            "insight_text": "No expense data available for this user."
        }

    expense_cols = [
        "Rent (USD)", "Groceries (USD)", "Eating Out (USD)", "Entertainment (USD)",
        "Subscription Services (USD)", "Education (USD)", "Online Shopping (USD)",
        "Savings (USD)", "Investments (USD)", "Travel (USD)", "Fitness (USD)", "Miscellaneous (USD)"
    ]

    current_expenses = user_exp[expense_cols].iloc[0].to_dict()
    total_expenses = sum(current_expenses.values())

    # If income column exists, use it; else estimate from total expenses
    total_income = float(user_exp.get("Income (USD)", pd.Series([total_expenses])).iloc[0])

    recommended_expenses = current_expenses.copy()

    # -------------------------------
    # Financial health rules
    # -------------------------------
    health_level = financial_row.get("financial_health") if financial_row is not None else "Moderate"

    if health_level == "Healthy":
        recommended_expenses["Savings (USD)"] += 0.05 * total_expenses
        recommended_expenses["Investments (USD)"] += 0.05 * total_expenses
    elif health_level == "Moderate":
        for col in ["Eating Out (USD)", "Entertainment (USD)", "Online Shopping (USD)"]:
            recommended_expenses[col] *= 0.7
        recommended_expenses["Savings (USD)"] += 0.05 * total_expenses
    else:  # At Risk
        for col in ["Eating Out (USD)", "Entertainment (USD)", "Online Shopping (USD)", "Travel (USD)"]:
            recommended_expenses[col] *= 0.5
        recommended_expenses["Savings (USD)"] += 0.1 * total_expenses

    # -------------------------------
    # 50/30/20 allocation
    # -------------------------------
    needs = ["Rent (USD)", "Groceries (USD)", "Education (USD)"]
    wants = ["Eating Out (USD)", "Entertainment (USD)", "Online Shopping (USD)",
             "Travel (USD)", "Subscription Services (USD)", "Fitness (USD)", "Miscellaneous (USD)"]
    savings_investments = ["Savings (USD)", "Investments (USD)"]

    needs_target = 0.5 * total_income
    wants_target = 0.3 * total_income
    savings_target = 0.2 * total_income

    def apply_scaled_allocation(categories, target_sum):
        current_sum = sum(recommended_expenses[c] for c in categories)
        if current_sum == 0:
            return
        scale = target_sum / current_sum
        for c in categories:
            new_value = recommended_expenses[c] * scale
            # Cap change to ±MAX_CHANGE_PERCENT
            max_inc = recommended_expenses[c] * (1 + MAX_CHANGE_PERCENT)
            max_dec = recommended_expenses[c] * (1 - MAX_CHANGE_PERCENT)
            recommended_expenses[c] = min(max(max_dec, new_value), max_inc)

    apply_scaled_allocation(needs, needs_target)
    apply_scaled_allocation(wants, wants_target)
    apply_scaled_allocation(savings_investments, savings_target)

    # -------------------------------
    # CRITICAL: Ensure total recommended expenses ≤ income
    # -------------------------------
    total_recommended = sum(recommended_expenses.values())
    was_scaled_to_income = False
    if total_recommended > total_income:
        was_scaled_to_income = True
        # Scale down all categories proportionally to fit within income
        scale_factor = total_income / total_recommended
        for cat in recommended_expenses:
            recommended_expenses[cat] = recommended_expenses[cat] * scale_factor
        
        # Round to 2 decimal places
        for cat in recommended_expenses:
            recommended_expenses[cat] = round(recommended_expenses[cat], 2)
        
        # Recalculate total after scaling (should now be ≤ income)
        total_recommended = sum(recommended_expenses.values())

    # -------------------------------
    # Human-readable insight text
    # -------------------------------
    behavior_type = behavior_row.get("behavior_type") if behavior_row is not None else "Unknown"
    behavior_risk = behavior_row.get("behavior_risk_level") if behavior_row is not None else "Unknown"
    financial_score = financial_row.get("health_score") if financial_row is not None else 0

    insight_lines = [
        f"Hello! Here's your personalized financial insight for next month:",
        f"- Spending behavior: '{behavior_type}' (Risk Level: {behavior_risk})",
        f"- Financial health: '{health_level}' (Score: {financial_score})",
        f"- Total Income: ${total_income:.2f} USD",
        f"- Total Expenses: ${total_expenses:.2f} USD",
        f"- Recommended Budget: ${total_recommended:.2f} USD (within income limit)",
        "",
    ]
    
    if was_scaled_to_income:
        insight_lines.append("⚠️ Note: Your recommended budget has been adjusted to fit within your income.")
        insight_lines.append("")
    
    insight_lines.append("Based on your current spending patterns and the 50/30/20 rule, we suggest the following adjustments:")

    for cat in expense_cols:
        current = current_expenses.get(cat, 0)
        recommended = recommended_expenses.get(cat, 0)
        if abs(current - recommended) > 1e-2:
            pct_change = (recommended - current) / (current + 1e-6) * 100 if current > 0 else 0
            if recommended > current:
                reason = "increase savings or investment focus" if cat in savings_investments else "adjust proportion to match financial health targets"
                insight_lines.append(
                    f"- {cat}: increase from {current:.2f} USD to {recommended:.2f} USD (+{pct_change:.1f}%) to {reason}."
                )
            else:
                reason = "reduce discretionary spending" if cat in wants else "adjust proportion to match financial health targets"
                insight_lines.append(
                    f"- {cat}: decrease from {current:.2f} USD to {recommended:.2f} USD ({pct_change:.1f}%) to {reason}."
                )

    # Highlight high discretionary spending
    for cat in wants:
        ratio = current_expenses.get(cat,0) / (total_expenses + 1e-6)
        if ratio > 0.2:
            insight_lines.append(f"* Note: {cat} makes up more than 20% of your total expenses, consider moderating it.")

    insight_lines.append("\nThese recommendations aim to help you balance your needs, wants, and savings while keeping financial health stable.")

    insight_text = "\n".join(insight_lines)

    return {
        "current_expenses": current_expenses,
        "recommended_expenses": recommended_expenses,
        "total_expenses": total_expenses,
        "income": total_income,
        "insight_text": insight_text
    }
