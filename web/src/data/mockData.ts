import { UserInsight } from '../types';

// Mock data for demonstration purposes
// This will be replaced with actual API calls later

export const mockUserInsight: UserInsight = {
  userId: "USER001",
  userName: "Alex Johnson",
  income: 5000,
  currentExpenses: [
    { name: "Rent", amount: 1500 },
    { name: "Groceries", amount: 450 },
    { name: "Eating Out", amount: 320 },
    { name: "Entertainment", amount: 180 },
    { name: "Subscription Services", amount: 85 },
    { name: "Education", amount: 200 },
    { name: "Online Shopping", amount: 250 },
    { name: "Savings", amount: 300 },
    { name: "Investments", amount: 150 },
    { name: "Travel", amount: 100 },
    { name: "Fitness", amount: 60 },
    { name: "Miscellaneous", amount: 120 }
  ],
  behaviorInsight: {
    type: "Impulsive Spender",
    riskLevel: "Medium",
    description: "You tend to make spontaneous purchases, especially in entertainment and online shopping categories. Consider implementing a 24-hour waiting period before non-essential purchases."
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
  recommendationText: `Based on your spending patterns and financial behavior analysis, we recommend the following adjustments for next month:

**Reduce Discretionary Spending:** Your current spending on Eating Out ($320), Entertainment ($180), and Online Shopping ($250) is significantly higher than recommended levels. We suggest reducing these by 37-44% to free up funds for more productive uses.

**Increase Savings & Investments:** Your current savings rate is below the recommended threshold. We suggest increasing your monthly savings from $300 to $500 (a 67% increase) and investments from $150 to $350 (a 133% increase). This will help build your emergency fund and long-term wealth.

**Subscription Audit:** Review your subscription services and consider canceling unused or underutilized subscriptions to reduce this expense from $85 to $50.

**Maintain Essential Categories:** Your rent, education, and fitness expenses are at appropriate levels and should be maintained.

By following these recommendations, you could improve your financial health score from 62 to an estimated 78 within the next 3-6 months.`
};

// Simulate API call delay
export const fetchUserInsight = async (userId: string): Promise<UserInsight | null> => {
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
    }, 1500);
  });
};
