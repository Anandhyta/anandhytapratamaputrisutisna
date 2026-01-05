// =========================================
// API Service - Backend Integration
// =========================================
// This service handles all API calls to the FastAPI backend
// Endpoint: /user_insight/{user_id}
// 
// Backend returns:
// {
//   user_id: number,
//   current_expenses: { "Rent (USD)": number, ... },
//   behavior_insight: { behavior_type, behavior_risk_level, behavior_details },
//   financial_insight: { financial_health, health_score, financial_risk_level, financial_details },
//   recommended_expenses: { "Rent (USD)": number, ... },
//   insight_text: string,
//   expense_changes: { category: { current, recommended, change_percent, change_amount } }
// }
// =========================================

// API Base URL - Configure this for your environment
// Development: http://localhost:8000
// Production: Your deployed API URL
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// =========================================
// API Response Types (matching backend)
// =========================================

/**
 * Raw response from backend API
 * These types match the Python Pydantic models exactly
 */
export interface ApiExpenseChanges {
  current: number;
  recommended: number;
  change_percent: number;
  change_amount: number;
}

export interface ApiBehaviorInsight {
  behavior_type: string;
  behavior_risk_level: string;
  behavior_details: string;
}

export interface ApiFinancialInsight {
  financial_health: string;
  health_score: number;
  financial_risk_level: string;
  financial_details: string;
}

export interface ApiUserInsightResponse {
  user_id: number;
  current_expenses: Record<string, number>;
  behavior_insight: ApiBehaviorInsight;
  financial_insight: ApiFinancialInsight;
  recommended_expenses: Record<string, number>;
  insight_text: string;
  expense_changes: Record<string, ApiExpenseChanges>;
  income?: number;
  total_expenses?: number;
}

// =========================================
// Error Types
// =========================================

export interface ApiError {
  status: number;
  message: string;
  detail?: string;
}

export class ApiException extends Error {
  public status: number;
  public detail?: string;

  constructor(status: number, message: string, detail?: string) {
    super(message);
    this.status = status;
    this.detail = detail;
    this.name = 'ApiException';
  }
}

// =========================================
// API Functions
// =========================================

/**
 * Fetch user financial insight from the backend API
 * 
 * @param userId - The user ID to fetch insights for
 * @returns Promise<ApiUserInsightResponse> - The complete user insight data
 * @throws ApiException if the request fails
 * 
 * Usage:
 * ```typescript
 * const data = await fetchUserInsight(16);
 * // data.current_expenses -> Current Expenses Page
 * // data.behavior_insight -> Behavior Insight Card
 * // data.financial_insight -> Financial Insight Card
 * // data.recommended_expenses -> Recommended Budget Page
 * // data.insight_text -> Recommendations Page
 * ```
 */
export async function fetchUserInsight(userId: string | number): Promise<ApiUserInsightResponse> {
  const url = `${API_BASE_URL}/user_insight/${userId}`;

  try {
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    });

    // Handle different HTTP status codes
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      
      if (response.status === 404) {
        throw new ApiException(
          404,
          `User ID ${userId} not found`,
          errorData.detail || 'The requested user does not exist in the database.'
        );
      }
      
      if (response.status === 500) {
        throw new ApiException(
          500,
          'Server error',
          errorData.detail || 'An internal server error occurred. Please try again later.'
        );
      }

      throw new ApiException(
        response.status,
        'Request failed',
        errorData.detail || `HTTP ${response.status}: ${response.statusText}`
      );
    }

    const data: ApiUserInsightResponse = await response.json();
    return data;

  } catch (error) {
    // Re-throw ApiException as-is
    if (error instanceof ApiException) {
      throw error;
    }

    // Handle network errors
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new ApiException(
        0,
        'Network error',
        'Unable to connect to the server. Please ensure the backend is running at ' + API_BASE_URL
      );
    }

    // Handle other errors
    throw new ApiException(
      0,
      'Unknown error',
      error instanceof Error ? error.message : 'An unexpected error occurred'
    );
  }
}

/**
 * Check if the API server is healthy
 * 
 * @returns Promise<boolean> - True if the server is healthy
 */
export async function checkApiHealth(): Promise<boolean> {
  try {
    const response = await fetch(`${API_BASE_URL}/`, {
      method: 'GET',
      headers: { 'Accept': 'application/json' },
    });
    return response.ok;
  } catch {
    return false;
  }
}

// =========================================
// Data Transformation Utilities
// =========================================

/**
 * Transform expense category name from backend format
 * "Rent (USD)" -> "Rent"
 */
export function cleanCategoryName(category: string): string {
  return category.replace(' (USD)', '').trim();
}

/**
 * Get category icon based on category name
 */
export function getCategoryIcon(category: string): string {
  const iconMap: Record<string, string> = {
    'Rent': '🏠',
    'Groceries': '🛒',
    'Eating Out': '🍽️',
    'Entertainment': '🎬',
    'Subscription Services': '📺',
    'Education': '📚',
    'Online Shopping': '🛍️',
    'Savings': '💰',
    'Investments': '📈',
    'Travel': '✈️',
    'Fitness': '💪',
    'Miscellaneous': '📦',
  };
  
  const cleanName = cleanCategoryName(category);
  return iconMap[cleanName] || '💵';
}

/**
 * Map risk level string to typed value
 */
export function mapRiskLevel(level: string): 'Low' | 'Medium' | 'High' | 'Very High' {
  const normalizedLevel = level.toLowerCase();
  if (normalizedLevel === 'low') return 'Low';
  if (normalizedLevel === 'medium' || normalizedLevel === 'moderate') return 'Medium';
  if (normalizedLevel === 'high') return 'High';
  if (normalizedLevel === 'very high' || normalizedLevel === 'critical') return 'Very High';
  return 'Medium'; // Default
}

/**
 * Map health level string to typed value
 */
export function mapHealthLevel(health: string): 'Poor' | 'Fair' | 'Good' | 'Excellent' | 'Critical' {
  const normalizedHealth = health.toLowerCase();
  if (normalizedHealth === 'critical') return 'Critical';
  if (normalizedHealth === 'at risk' || normalizedHealth === 'poor') return 'Poor';
  if (normalizedHealth === 'moderate' || normalizedHealth === 'fair') return 'Fair';
  if (normalizedHealth === 'healthy' || normalizedHealth === 'good') return 'Good';
  if (normalizedHealth === 'excellent') return 'Excellent';
  return 'Fair'; // Default
}
