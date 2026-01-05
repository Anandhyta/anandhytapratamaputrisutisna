// =========================================
// Types for the Financial Insight Dashboard
// =========================================
// These types are used throughout the frontend to ensure type safety
// They are mapped from the backend API response

// =========================================
// EXPENSE TYPES
// =========================================

/**
 * Individual expense category with amount and optional icon
 * Mapped from: API current_expenses or recommended_expenses
 */
export interface ExpenseCategory {
  name: string;           // Category name (e.g., "Rent", "Groceries")
  amount: number;         // Amount in USD
  icon?: string;          // Emoji icon for display
}

// =========================================
// INSIGHT TYPES
// =========================================

/**
 * Behavior Insight from spending pattern analysis
 * Mapped from: API behavior_insight
 * 
 * Backend fields -> Frontend fields:
 * - behavior_type -> type
 * - behavior_risk_level -> riskLevel
 * - behavior_details -> description
 */
export interface BehaviorInsight {
  type: string;                                          // e.g., "Impulsive Spender", "Balanced", "Consistently Overspending"
  riskLevel: 'Low' | 'Medium' | 'High' | 'Very High';   // Normalized risk level
  description: string;                                   // Detailed justification
}

/**
 * Financial Insight from financial health analysis
 * Mapped from: API financial_insight
 * 
 * Backend fields -> Frontend fields:
 * - financial_health -> healthLevel
 * - financial_risk_level -> riskLevel  
 * - health_score -> healthScore
 * - financial_details -> (used in description, can extend)
 */
export interface FinancialInsight {
  healthLevel: 'Poor' | 'Fair' | 'Good' | 'Excellent' | 'Critical';  // Mapped from financial_health
  riskLevel: 'Low' | 'Medium' | 'High' | 'Very High';                // Normalized risk level
  healthScore: number;                                                // Score (can be negative for critical)
  description?: string;                                               // Optional: financial_details
}

// =========================================
// BUDGET RECOMMENDATION TYPES
// =========================================

/**
 * Budget recommendation for a single category
 * Mapped from: API expense_changes[category]
 * 
 * Backend fields -> Frontend fields:
 * - category key -> category
 * - expense_changes[cat].current -> currentAmount
 * - expense_changes[cat].recommended -> recommendedAmount
 * - expense_changes[cat].change_percent -> percentageChange
 */
export interface BudgetRecommendation {
  category: string;           // Category name (cleaned, without " (USD)")
  currentAmount: number;      // Current spending amount
  recommendedAmount: number;  // Recommended spending amount
  percentageChange: number;   // % change (positive = increase, negative = decrease)
}

// =========================================
// COMPLETE USER INSIGHT
// =========================================

/**
 * Complete user insight combining all data
 * This is the main type used by the Dashboard component
 * 
 * Mapped from: API /user_insight/{user_id} response
 * 
 * Field mappings:
 * - user_id -> userId (converted to string)
 * - (not from API) -> userName (optional display name)
 * - income from recommendation.py -> income
 * - total_expenses calculated -> totalExpenses
 * - current_expenses -> currentExpenses (transformed to ExpenseCategory[])
 * - behavior_insight -> behaviorInsight (transformed)
 * - financial_insight -> financialInsight (transformed)
 * - expense_changes -> budgetRecommendations (transformed to BudgetRecommendation[])
 * - insight_text -> recommendationText
 */
export interface UserInsight {
  userId: string;                                // User identifier
  userName?: string;                             // Optional display name
  income: number;                                // Monthly income in USD
  totalExpenses?: number;                        // Total of all expenses
  currentExpenses: ExpenseCategory[];            // Array of current expense categories
  behaviorInsight: BehaviorInsight;              // Behavior analysis
  financialInsight: FinancialInsight;            // Financial health analysis
  budgetRecommendations: BudgetRecommendation[]; // Category-wise recommendations
  recommendationText: string;                    // Human-readable advice
}

// =========================================
// API STATE TYPES (for React components)
// =========================================

/**
 * Loading state for async operations
 */
export type LoadingState = 'idle' | 'loading' | 'success' | 'error';

/**
 * Error state for API errors
 */
export interface ErrorState {
  message: string;
  detail?: string;
  code?: number;
}

