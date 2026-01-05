# =========================================
# api_server.py - FastAPI Backend Server
# Purpose:
#   Expose RESTful API endpoints for the Flutter mobile/desktop app
#   Main endpoint: /user_insight/{user_id}
#   Returns comprehensive financial insights including:
#     - Current expenses
#     - Behavior insight
#     - Financial insight
#     - Recommended budget
#     - Human-readable recommendation text
# =========================================

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Optional
import pandas as pd
import uvicorn

# Import existing modules
from get_user_insight import get_user_insight
from recommendation import generate_financial_recommendation

# ===============================
# FASTAPI APP INITIALIZATION
# ===============================
app = FastAPI(
    title="Financial Insight API",
    description="API for personalized financial recommendations and insights",
    version="1.0.0"
)

# Enable CORS for Flutter app to connect from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (mobile/desktop apps)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===============================
# RESPONSE MODELS
# ===============================
class BehaviorInsight(BaseModel):
    behavior_type: str
    behavior_risk_level: str
    behavior_details: str

class FinancialInsight(BaseModel):
    financial_health: str
    health_score: float
    financial_risk_level: str
    financial_details: str

class UserInsightResponse(BaseModel):
    user_id: int
    current_expenses: Dict[str, float]
    behavior_insight: BehaviorInsight
    financial_insight: FinancialInsight
    recommended_expenses: Dict[str, float]
    insight_text: str
    expense_changes: Dict[str, dict]  # Category -> {current, recommended, change_percent}

# ===============================
# API ENDPOINTS
# ===============================

@app.get("/")
async def root():
    """
    Root endpoint - API health check
    """
    return {
        "message": "Financial Insight API is running",
        "version": "1.0.0",
        "endpoints": {
            "user_insight": "/user_insight/{user_id}",
            "docs": "/docs"
        }
    }

@app.get("/user_insight/{user_id}", response_model=UserInsightResponse)
async def get_user_financial_insight(user_id: int):
    """
    Get comprehensive financial insight for a specific user
    
    Args:
        user_id: Unique identifier for the user
    
    Returns:
        UserInsightResponse containing:
        - current_expenses: All expense categories
        - behavior_insight: Spending behavior analysis
        - financial_insight: Financial health metrics
        - recommended_expenses: Optimized budget recommendations
        - insight_text: Human-readable explanation
        - expense_changes: Detailed breakdown of budget changes
    
    Raises:
        HTTPException: If user_id not found or data unavailable
    """
    try:
        # Get user insights from existing modules
        insight_data = get_user_insight(user_id)
        
        if insight_data is None:
            raise HTTPException(
                status_code=404,
                detail=f"User ID {user_id} not found in database"
            )
        
        # Extract components
        behavior_insight = insight_data.get("behavior_insight", {})
        financial_insight = insight_data.get("financial_insight", {})
        
        # Generate financial recommendation
        recommendation = generate_financial_recommendation(
            user_id=user_id,
            behavior_row=behavior_insight,
            financial_row=financial_insight
        )
        
        current_expenses = recommendation.get("current_expenses")
        recommended_expenses = recommendation.get("recommended_expenses")
        insight_text = recommendation.get("insight_text")
        
        if current_expenses is None:
            raise HTTPException(
                status_code=404,
                detail=f"No expense data available for user ID {user_id}"
            )
        
        # Calculate expense changes with percentages
        expense_changes = {}
        for category in current_expenses.keys():
            current = current_expenses[category]
            recommended = recommended_expenses[category]
            change_percent = 0.0
            if current > 0:
                change_percent = ((recommended - current) / current) * 100
            
            expense_changes[category] = {
                "current": round(current, 2),
                "recommended": round(recommended, 2),
                "change_percent": round(change_percent, 2),
                "change_amount": round(recommended - current, 2)
            }
        
        # Build response
        response = UserInsightResponse(
            user_id=user_id,
            current_expenses=current_expenses,
            behavior_insight=BehaviorInsight(
                behavior_type=behavior_insight.get("behavior_type", "Unknown"),
                behavior_risk_level=behavior_insight.get("behavior_risk_level", "Unknown"),
                behavior_details=behavior_insight.get("behavior_details", "No details available")
            ),
            financial_insight=FinancialInsight(
                financial_health=financial_insight.get("financial_health", "Unknown"),
                health_score=financial_insight.get("health_score", 0.0),
                financial_risk_level=financial_insight.get("financial_risk_level", "Unknown"),
                financial_details=financial_insight.get("financial_details", "No details available")
            ),
            recommended_expenses=recommended_expenses,
            insight_text=insight_text,
            expense_changes=expense_changes
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

# ===============================
# RUN SERVER
# ===============================
if __name__ == "__main__":
    print("=" * 60)
    print("Starting Financial Insight API Server")
    print("=" * 60)
    print("Access API at: http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    print("=" * 60)
    
    uvicorn.run(
        app,
        host="0.0.0.0",  # Accept connections from any IP (for mobile testing)
        port=8000,
        log_level="info"
    )
