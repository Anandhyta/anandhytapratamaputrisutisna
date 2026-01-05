import React from 'react';
import { ExpenseCategory } from '../../types';
import './CurrentExpenses.css';

// Icon mapping for expense categories
const getCategoryIcon = (category: string): string => {
  const icons: Record<string, string> = {
    'Rent': '🏠',
    'Groceries': '🛒',
    'Eating Out': '🍽️',
    'Entertainment': '🎬',
    'Subscription Services': '📱',
    'Education': '📚',
    'Online Shopping': '🛍️',
    'Savings': '💰',
    'Investments': '📈',
    'Travel': '✈️',
    'Fitness': '💪',
    'Miscellaneous': '📦'
  };
  return icons[category] || '💵';
};

// Categories that are considered discretionary (high spending warning)
const discretionaryCategories = [
  'Eating Out',
  'Entertainment',
  'Online Shopping',
  'Subscription Services',
  'Travel'
];

interface CurrentExpensesProps {
  expenses: ExpenseCategory[];
  income: number;
}

const CurrentExpenses: React.FC<CurrentExpensesProps> = ({ expenses, income }) => {
  const totalExpenses = expenses.reduce((sum, exp) => sum + exp.amount, 0);
  
  // Calculate overspending
  const isOverspending = totalExpenses > income;
  const overspendingAmount = totalExpenses - income;
  const overspendingPercentage = income > 0 ? ((overspendingAmount / income) * 100) : 0;
  const savingsPercentage = income > 0 ? (((income - totalExpenses) / income) * 100) : 0;

  const isHighDiscretionary = (category: string, amount: number): boolean => {
    if (!discretionaryCategories.includes(category)) return false;
    // Consider high if more than 5% of total expenses
    return (amount / totalExpenses) > 0.05;
  };

  return (
    <div className="current-expenses">
      {/* Income & Summary Section */}
      <div className="income-summary">
        <div className="summary-card income-card">
          <span className="summary-icon">💵</span>
          <div className="summary-details">
            <span className="summary-label">Monthly Income</span>
            <span className="summary-value income-value">${income.toLocaleString()}</span>
          </div>
        </div>
        <div className="summary-card expenses-card">
          <span className="summary-icon">💳</span>
          <div className="summary-details">
            <span className="summary-label">Total Expenses</span>
            <span className="summary-value expenses-value">${totalExpenses.toLocaleString()}</span>
          </div>
        </div>
        {/* Overspending / Savings Indicator */}
        <div className={`summary-card spending-status-card ${isOverspending ? 'overspending' : 'under-budget'}`}>
          <span className="summary-icon">{isOverspending ? '⚠️' : '✅'}</span>
          <div className="summary-details">
            <span className="summary-label">{isOverspending ? 'Overspending' : 'Under Budget'}</span>
            <span className={`summary-value ${isOverspending ? 'overspending-value' : 'savings-value'}`}>
              {isOverspending 
                ? `+${overspendingPercentage.toFixed(1)}%` 
                : `-${savingsPercentage.toFixed(1)}%`}
            </span>
            <span className="summary-amount">
              {isOverspending 
                ? `$${overspendingAmount.toLocaleString()} over` 
                : `$${(income - totalExpenses).toLocaleString()} saved`}
            </span>
          </div>
        </div>
      </div>

      <div className="section-header">
        <h2>💳 Expense Breakdown</h2>
      </div>
      
      <div className="expenses-grid">
        {expenses.map((expense, index) => (
          <div 
            key={index} 
            className={`expense-card ${isHighDiscretionary(expense.name, expense.amount) ? 'high-discretionary' : ''}`}
          >
            <div className="expense-icon">{getCategoryIcon(expense.name)}</div>
            <div className="expense-details">
              <span className="expense-name">{expense.name}</span>
              <span className="expense-amount">${expense.amount.toLocaleString()}</span>
            </div>
            {isHighDiscretionary(expense.name, expense.amount) && (
              <div className="warning-badge" title="High discretionary spending">
                ⚠️
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default CurrentExpenses;
