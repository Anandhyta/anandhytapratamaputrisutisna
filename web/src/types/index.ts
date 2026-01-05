// Types for the Financial Insight Dashboard

export interface ExpenseCategory {
  name: string;
  amount: number;
  icon?: string;
}

export interface BehaviorInsight {
  type: string;
  riskLevel: 'Low' | 'Medium' | 'High';
  description: string;
}

export interface FinancialInsight {
  healthLevel: 'Poor' | 'Fair' | 'Good' | 'Excellent';
  riskLevel: 'Low' | 'Medium' | 'High';
  healthScore: number;
}

export interface BudgetRecommendation {
  category: string;
  currentAmount: number;
  recommendedAmount: number;
  percentageChange: number;
}

export interface UserInsight {
  userId: string;
  userName?: string;
  income: number;
  currentExpenses: ExpenseCategory[];
  behaviorInsight: BehaviorInsight;
  financialInsight: FinancialInsight;
  budgetRecommendations: BudgetRecommendation[];
  recommendationText: string;
}
