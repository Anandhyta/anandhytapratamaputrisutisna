import React from 'react';
import { BudgetRecommendation } from '../../types';
import './RecommendedBudget.css';

interface RecommendedBudgetProps {
  recommendations: BudgetRecommendation[];
}

const RecommendedBudget: React.FC<RecommendedBudgetProps> = ({ recommendations }) => {
  const currentTotal = recommendations.reduce((sum, r) => sum + r.currentAmount, 0);
  const recommendedTotal = recommendations.reduce((sum, r) => sum + r.recommendedAmount, 0);
  const totalChange = ((recommendedTotal - currentTotal) / currentTotal) * 100;

  const getChangeClass = (change: number): string => {
    if (change > 0) return 'increase';
    if (change < 0) return 'decrease';
    return 'no-change';
  };

  const formatChange = (change: number): string => {
    if (change > 0) return `+${change.toFixed(1)}%`;
    if (change < 0) return `${change.toFixed(1)}%`;
    return '—';
  };

  return (
    <div className="recommended-budget">
      <div className="section-header">
        <h2>📋 Recommended Budget (Next Month)</h2>
        <div className="summary-badges">
          <div className="summary-badge current">
            Current: <span>${currentTotal.toLocaleString()}</span>
          </div>
          <div className="summary-badge recommended">
            Recommended: <span>${recommendedTotal.toLocaleString()}</span>
          </div>
        </div>
      </div>

      <div className="budget-table-container">
        <table className="budget-table">
          <thead>
            <tr>
              <th>Category</th>
              <th>Current</th>
              <th>Recommended</th>
              <th>Change</th>
            </tr>
          </thead>
          <tbody>
            {recommendations.map((rec, index) => (
              <tr key={index} className={getChangeClass(rec.percentageChange)}>
                <td className="category-cell">
                  <span className="category-name">{rec.category}</span>
                  {rec.percentageChange !== 0 && (
                    <span className={`change-indicator ${getChangeClass(rec.percentageChange)}`}>
                      {rec.percentageChange > 0 ? '↑' : '↓'}
                    </span>
                  )}
                </td>
                <td className="amount-cell">${rec.currentAmount.toLocaleString()}</td>
                <td className="amount-cell recommended-cell">
                  ${rec.recommendedAmount.toLocaleString()}
                </td>
                <td className={`change-cell ${getChangeClass(rec.percentageChange)}`}>
                  {formatChange(rec.percentageChange)}
                </td>
              </tr>
            ))}
          </tbody>
          <tfoot>
            <tr className="total-row">
              <td><strong>Total</strong></td>
              <td><strong>${currentTotal.toLocaleString()}</strong></td>
              <td><strong>${recommendedTotal.toLocaleString()}</strong></td>
              <td className={`change-cell ${getChangeClass(totalChange)}`}>
                <strong>{formatChange(totalChange)}</strong>
              </td>
            </tr>
          </tfoot>
        </table>
      </div>

      {/* Mobile Card View */}
      <div className="budget-cards-mobile">
        {recommendations.map((rec, index) => (
          <div key={index} className={`budget-card-mobile ${getChangeClass(rec.percentageChange)}`}>
            <div className="card-category">
              <span>{rec.category}</span>
              {rec.percentageChange !== 0 && (
                <span className={`change-badge ${getChangeClass(rec.percentageChange)}`}>
                  {formatChange(rec.percentageChange)}
                </span>
              )}
            </div>
            <div className="card-amounts">
              <div className="amount-group">
                <span className="amount-label">Current</span>
                <span className="amount-value">${rec.currentAmount.toLocaleString()}</span>
              </div>
              <div className="arrow">→</div>
              <div className="amount-group">
                <span className="amount-label">Recommended</span>
                <span className="amount-value recommended">${rec.recommendedAmount.toLocaleString()}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default RecommendedBudget;
