// =========================================
// Data Service - API Integration
// =========================================
// This module handles fetching and transforming data from the backend API
// 
// API Endpoint: GET /user_insight/{user_id}
// Backend returns raw data that needs to be transformed to match frontend types
// =========================================

import { UserInsight, ExpenseCategory, BudgetRecommendation } from '../types';
import { 
  fetchUserInsight as apiFetchUserInsight,
  ApiUserInsightResponse,
  cleanCategoryName,
  getCategoryIcon,
  mapRiskLevel,
  mapHealthLevel,
  ApiException
} from '../services/api';

// =========================================
// DATA TRANSFORMATION FUNCTIONS
// =========================================

/**
 * Transform API expense object to ExpenseCategory array
 * 
 * Input (from API):
 * {
 *   "Rent (USD)": 1500,
 *   "Groceries (USD)": 450,
 *   ...
 * }
 * 
 * Output (for frontend):
 * [
 *   { name: "Rent", amount: 1500, icon: "🏠" },
 *   { name: "Groceries", amount: 450, icon: "🛒" },
 *   ...
 * ]
 */
function transformExpenses(expenses: Record<string, number>): ExpenseCategory[] {
  return Object.entries(expenses).map(([category, amount]) => ({
    name: cleanCategoryName(category),
    amount: Number(amount.toFixed(2)),
    icon: getCategoryIcon(category),
  }));
}

/**
 * Transform API expense_changes to BudgetRecommendation array
 * 
 * Input (from API):
 * {
 *   "Rent (USD)": { current: 1500, recommended: 1500, change_percent: 0, change_amount: 0 },
 *   ...
 * }
 * 
 * Output (for frontend):
 * [
 *   { category: "Rent", currentAmount: 1500, recommendedAmount: 1500, percentageChange: 0 },
 *   ...
 * ]
 */
function transformBudgetRecommendations(
  expenseChanges: Record<string, { current: number; recommended: number; change_percent: number }>
): BudgetRecommendation[] {
  return Object.entries(expenseChanges).map(([category, data]) => ({
    category: cleanCategoryName(category),
    currentAmount: Number(data.current.toFixed(2)),
    recommendedAmount: Number(data.recommended.toFixed(2)),
    percentageChange: Number(data.change_percent.toFixed(1)),
  }));
}

/**
 * Transform complete API response to UserInsight
 * This is the main transformation function that maps all API fields to frontend types
 * 
 * Field Mappings:
 * ---------------
 * API Field                    -> Frontend Field
 * user_id                      -> userId (string)
 * income                       -> income
 * current_expenses             -> currentExpenses (transformed)
 * behavior_insight.behavior_type      -> behaviorInsight.type
 * behavior_insight.behavior_risk_level -> behaviorInsight.riskLevel (mapped)
 * behavior_insight.behavior_details    -> behaviorInsight.description
 * financial_insight.financial_health   -> financialInsight.healthLevel (mapped)
 * financial_insight.health_score       -> financialInsight.healthScore
 * financial_insight.financial_risk_level -> financialInsight.riskLevel (mapped)
 * financial_insight.financial_details    -> financialInsight.description
 * expense_changes              -> budgetRecommendations (transformed)
 * insight_text                 -> recommendationText
 */
function transformApiResponse(apiData: ApiUserInsightResponse): UserInsight {
  // Calculate total expenses if not provided
  const totalExpenses = apiData.total_expenses || 
    Object.values(apiData.current_expenses).reduce((sum, val) => sum + val, 0);

  // Estimate income if not provided (use total expenses as fallback)
  const income = apiData.income || totalExpenses;

  return {
    // User identification
    userId: String(apiData.user_id),
    
    // Financial overview
    income: Number(income.toFixed(2)),
    totalExpenses: Number(totalExpenses.toFixed(2)),
    
    // Current Expenses Page
    // Maps to: CurrentExpenses component
    currentExpenses: transformExpenses(apiData.current_expenses),
    
    // Behavior Insight
    // Maps to: InsightCards component (Behavior card)
    behaviorInsight: {
      type: apiData.behavior_insight.behavior_type,
      riskLevel: mapRiskLevel(apiData.behavior_insight.behavior_risk_level),
      description: apiData.behavior_insight.behavior_details,
    },
    
    // Financial Insight
    // Maps to: InsightCards component (Financial card)
    financialInsight: {
      healthLevel: mapHealthLevel(apiData.financial_insight.financial_health),
      riskLevel: mapRiskLevel(apiData.financial_insight.financial_risk_level),
      healthScore: Number(apiData.financial_insight.health_score.toFixed(1)),
      description: apiData.financial_insight.financial_details,
    },
    
    // Recommended Budget Page
    // Maps to: RecommendedBudget component
    budgetRecommendations: transformBudgetRecommendations(apiData.expense_changes),
    
    // Recommendations Page
    // Maps to: RecommendationText component
    recommendationText: apiData.insight_text,
  };
}

// =========================================
// PUBLIC API FUNCTION
// =========================================

/**
 * Fetch user insight from the backend API
 * 
 * This is the main function called by the Dashboard component
 * It handles:
 * 1. Making the API request
 * 2. Transforming the response to frontend types
 * 3. Error handling
 * 
 * @param userId - The user ID to fetch insights for
 * @returns Promise<UserInsight | null> - Transformed user insight or null if not found
 * @throws Error with user-friendly message if API fails
 * 
 * Usage in Dashboard.tsx:
 * ```typescript
 * const result = await fetchUserInsight(userId);
 * if (result) {
 *   setUserInsight(result);
 * }
 * ```
 */
export const fetchUserInsight = async (userId: string): Promise<UserInsight | null> => {
  // Validate input
  if (!userId.trim()) {
    return null;
  }

  try {
    // Fetch from API
    const apiResponse = await apiFetchUserInsight(userId);
    
    // Transform to frontend types
    const userInsight = transformApiResponse(apiResponse);
    
    return userInsight;
    
  } catch (error) {
    // Handle API errors
    if (error instanceof ApiException) {
      if (error.status === 404) {
        // User not found - return null (Dashboard will show "not found" message)
        return null;
      }
      // Other API errors - throw with details
      throw new Error(error.detail || error.message);
    }
    
    // Unknown errors
    throw new Error(
      error instanceof Error 
        ? error.message 
        : 'An unexpected error occurred while fetching user data'
    );
  }
};

// =========================================
// MOCK DATA (for development/testing without backend)
// =========================================

/**
 * Mock user insight for development without backend
 * Set USE_MOCK_DATA = true to use this instead of real API
 */
export const USE_MOCK_DATA = false; // Set to true to use mock data

export const mockUserInsight: UserInsight = {
  userId: "16",
  userName: "Test User",
  income: 5000,
  totalExpenses: 3715,
  currentExpenses: [
    { name: "Rent", amount: 1500, icon: "🏠" },
    { name: "Groceries", amount: 450, icon: "🛒" },
    { name: "Eating Out", amount: 320, icon: "🍽️" },
    { name: "Entertainment", amount: 180, icon: "🎬" },
    { name: "Subscription Services", amount: 85, icon: "📺" },
    { name: "Education", amount: 200, icon: "📚" },
    { name: "Online Shopping", amount: 250, icon: "🛍️" },
    { name: "Savings", amount: 300, icon: "💰" },
    { name: "Investments", amount: 150, icon: "📈" },
    { name: "Travel", amount: 100, icon: "✈️" },
    { name: "Fitness", amount: 60, icon: "💪" },
    { name: "Miscellaneous", amount: 120, icon: "📦" }
  ],
  behaviorInsight: {
    type: "Impulsive Spender",
    riskLevel: "Medium",
    description: "You tend to make spontaneous purchases, especially in entertainment and online shopping categories."
  },
  financialInsight: {
    healthLevel: "Fair",
    riskLevel: "Medium",
    healthScore: 62
  },
  budgetRecommendations: [
    { category: "Rent", currentAmount: 1500, recommendedAmount: 1500, percentageChange: 0 },
    { category: "Groceries", currentAmount: 450, recommendedAmount: 400, percentageChange: -11.1 },
    { category: "Eating Out", currentAmount: 320, recommendedAmount: 200, percentageChange: -37.5 },
    { category: "Entertainment", currentAmount: 180, recommendedAmount: 100, percentageChange: -44.4 },
    { category: "Subscription Services", currentAmount: 85, recommendedAmount: 50, percentageChange: -41.2 },
    { category: "Education", currentAmount: 200, recommendedAmount: 200, percentageChange: 0 },
    { category: "Online Shopping", currentAmount: 250, recommendedAmount: 150, percentageChange: -40 },
    { category: "Savings", currentAmount: 300, recommendedAmount: 500, percentageChange: 66.7 },
    { category: "Investments", currentAmount: 150, recommendedAmount: 350, percentageChange: 133.3 },
    { category: "Travel", currentAmount: 100, recommendedAmount: 80, percentageChange: -20 },
    { category: "Fitness", currentAmount: 60, recommendedAmount: 60, percentageChange: 0 },
    { category: "Miscellaneous", currentAmount: 120, recommendedAmount: 80, percentageChange: -33.3 }
  ],
  recommendationText: `Hello! Here's your personalized financial insight for next month:

Based on your spending patterns and the 50/30/20 rule, we suggest the following adjustments:

- Eating Out: decrease from 320.00 USD to 200.00 USD (-37.5%) to reduce discretionary spending.
- Entertainment: decrease from 180.00 USD to 100.00 USD (-44.4%) to reduce discretionary spending.
- Online Shopping: decrease from 250.00 USD to 150.00 USD (-40.0%) to reduce discretionary spending.
- Savings: increase from 300.00 USD to 500.00 USD (+66.7%) to increase savings focus.
- Investments: increase from 150.00 USD to 350.00 USD (+133.3%) to increase investment focus.

These recommendations aim to help you balance your needs, wants, and savings while keeping financial health stable.`
};

/**
 * Fetch mock data (for development)
 * Used when USE_MOCK_DATA = true
 */
export const fetchMockUserInsight = async (userId: string): Promise<UserInsight | null> => {
  return new Promise((resolve) => {
    setTimeout(() => {
      if (userId.trim()) {
        resolve({
          ...mockUserInsight,
          userId: userId
        });
      } else {
        resolve(null);
      }
    }, 1000); // Simulate network delay
  });
};

