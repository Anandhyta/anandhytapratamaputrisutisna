# insight_text.py

def generate_insight_text(behavior_row, financial_row):
    """
    Generate a human-readable insight text combining behavioral and financial analysis.

    Parameters:
    - behavior_row (pd.Series or dict): one user's behavioral insight
    - financial_row (pd.Series or dict): one user's financial insight

    Returns:
    - str: insight text paragraph
    """

    # -----------------------------
    # Extract behavior information
    # -----------------------------
    behavior_type = behavior_row.get("behavior_type", "Unknown")
    behavior_risk = behavior_row.get("behavior_risk_level", "Unknown")

    # -----------------------------
    # Extract financial information
    # -----------------------------
    financial_health = financial_row.get("financial_health", "Unknown")
    financial_risk = financial_row.get("financial_risk_level", "Unknown")
    health_score = financial_row.get("health_score", None)
    justification = financial_row.get("health_justification", "")

    insight_parts = []

    # =============================
    # Behavioral Insight Section
    # =============================
    if behavior_risk == "Low":
        insight_parts.append(
            "The user demonstrates stable and consistent spending behavior with minimal behavioral risk."
        )
    elif behavior_risk == "Medium":
        insight_parts.append(
            "The user's spending behavior shows moderate variability, indicating occasional inconsistencies that may affect financial stability."
        )
    elif behavior_risk == "High":
        insight_parts.append(
            "The user's spending behavior is highly inconsistent, reflecting elevated behavioral risk and irregular financial patterns."
        )
    else:
        insight_parts.append(
            "The user's spending behavior could not be clearly classified due to insufficient or ambiguous data."
        )

    # =============================
    # Financial Health Section
    # =============================
    if financial_health == "Healthy":
        insight_parts.append(
            "From a financial perspective, the user is in a healthy condition, supported by balanced spending and adequate financial reserves."
        )
    elif financial_health == "Moderate":
        insight_parts.append(
            "Financially, the user is in a moderate condition, where overall stability is present but there is room for improvement in financial management."
        )
    elif financial_health == "At Risk":
        insight_parts.append(
            "From a financial standpoint, the user is at risk, suggesting potential challenges in sustaining long-term financial well-being."
        )
    else:
        insight_parts.append(
            "The user's overall financial condition could not be conclusively determined."
        )

    # =============================
    # Cross-Insight Logic (IMPORTANT)
    # =============================
    if behavior_risk == "Low" and financial_risk == "High":
        insight_parts.append(
            "Despite disciplined spending behavior, financial indicators suggest underlying risks that may stem from income constraints or high fixed expenses."
        )

    if behavior_risk == "High" and financial_risk == "Low":
        insight_parts.append(
            "Although current financial health appears stable, inconsistent spending behavior may pose risks if left unaddressed."
        )

    # =============================
    # Score-based Refinement
    # =============================
    if isinstance(health_score, (int, float)):
        if health_score >= 75:
            insight_parts.append(
                "The financial health score reflects strong financial resilience and effective resource allocation."
            )
        elif 50 <= health_score < 75:
            insight_parts.append(
                "The financial health score indicates an average level of financial resilience with moderate exposure to financial stress."
            )
        else:
            insight_parts.append(
                "The financial health score highlights significant vulnerability, emphasizing the need for corrective financial actions."
            )

    # =============================
    # Justification (Optional but Valuable)
    # =============================
    if justification:
        insight_parts.append(justification)

    # -----------------------------
    # Final Insight Text
    # -----------------------------
    insight_text = " ".join(insight_parts)

    return insight_text
