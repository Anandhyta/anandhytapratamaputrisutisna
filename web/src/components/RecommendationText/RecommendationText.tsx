import React from 'react';
import './RecommendationText.css';

interface RecommendationTextProps {
  text: string;
}

interface ParsedRecommendation {
  greeting: string;
  behavior: { type: string; risk: string };
  health: { level: string; score: string };
  income: string;
  expenses: string;
  recommendedBudget: string;
  wasScaled: boolean;
  changes: { category: string; from: string; to: string; percent: string; direction: 'increase' | 'decrease'; reason: string }[];
  notes: string[];
  closing: string;
}

const RecommendationText: React.FC<RecommendationTextProps> = ({ text }) => {
  // Parse the insight text into structured data
  const parseInsightText = (rawText: string): ParsedRecommendation => {
    const lines = rawText.split('\n').filter(l => l.trim());
    
    const result: ParsedRecommendation = {
      greeting: '',
      behavior: { type: 'Unknown', risk: 'Unknown' },
      health: { level: 'Unknown', score: '0' },
      income: '$0',
      expenses: '$0',
      recommendedBudget: '$0',
      wasScaled: false,
      changes: [],
      notes: [],
      closing: ''
    };

    lines.forEach(line => {
      const trimmed = line.trim();
      
      // Greeting
      if (trimmed.startsWith('Hello!')) {
        result.greeting = trimmed;
      }
      // Behavior
      else if (trimmed.includes('Spending behavior:')) {
        const match = trimmed.match(/Spending behavior: '([^']+)' \(Risk Level: ([^)]+)\)/);
        if (match) {
          result.behavior = { type: match[1], risk: match[2] };
        }
      }
      // Health
      else if (trimmed.includes('Financial health:')) {
        const match = trimmed.match(/Financial health: '([^']+)' \(Score: ([^)]+)\)/);
        if (match) {
          result.health = { level: match[1], score: match[2] };
        }
      }
      // Income
      else if (trimmed.includes('Total Income:')) {
        const match = trimmed.match(/Total Income: \$?([\d,.]+)/);
        if (match) result.income = `$${parseFloat(match[1]).toLocaleString()}`;
      }
      // Expenses
      else if (trimmed.includes('Total Expenses:') && !trimmed.includes('Recommended')) {
        const match = trimmed.match(/Total Expenses: \$?([\d,.]+)/);
        if (match) result.expenses = `$${parseFloat(match[1]).toLocaleString()}`;
      }
      // Recommended Budget
      else if (trimmed.includes('Recommended Budget:')) {
        const match = trimmed.match(/Recommended Budget: \$?([\d,.]+)/);
        if (match) result.recommendedBudget = `$${parseFloat(match[1]).toLocaleString()}`;
      }
      // Was scaled warning
      else if (trimmed.includes('⚠️') && trimmed.includes('adjusted to fit')) {
        result.wasScaled = true;
      }
      // Category changes
      else if (trimmed.startsWith('- ') && (trimmed.includes('decrease from') || trimmed.includes('increase from'))) {
        const isIncrease = trimmed.includes('increase from');
        const match = trimmed.match(/- ([^:]+): (increase|decrease) from ([\d.]+) USD to ([\d.]+) USD \(([+-]?[\d.]+%)\) to (.+)\./);
        if (match) {
          result.changes.push({
            category: match[1].replace(' (USD)', ''),
            from: `$${parseFloat(match[3]).toLocaleString()}`,
            to: `$${parseFloat(match[4]).toLocaleString()}`,
            percent: match[5],
            direction: isIncrease ? 'increase' : 'decrease',
            reason: match[6]
          });
        }
      }
      // Notes
      else if (trimmed.startsWith('* Note:')) {
        result.notes.push(trimmed.replace('* Note:', '').trim());
      }
      // Closing
      else if (trimmed.includes('These recommendations aim')) {
        result.closing = trimmed;
      }
    });

    return result;
  };

  const parsed = parseInsightText(text);
  
  // Separate increases and decreases
  const increases = parsed.changes.filter(c => c.direction === 'increase');
  const decreases = parsed.changes.filter(c => c.direction === 'decrease');

  const getBehaviorColor = (risk: string) => {
    switch (risk.toLowerCase()) {
      case 'low': return 'status-good';
      case 'medium': return 'status-warning';
      case 'high': return 'status-danger';
      default: return 'status-neutral';
    }
  };

  const getHealthColor = (level: string) => {
    switch (level.toLowerCase()) {
      case 'healthy': return 'status-good';
      case 'moderate': return 'status-warning';
      case 'at risk': return 'status-danger';
      default: return 'status-neutral';
    }
  };

  return (
    <div className="recommendation-text">
      <div className="section-header">
        <h2>💡 Personalized Recommendations</h2>
        <button className="export-btn" title="Export as PDF (UI only)">
          <span className="export-icon">📄</span>
          Export PDF
        </button>
      </div>

      {/* Summary Cards */}
      <div className="insight-summary-cards">
        <div className={`insight-card ${getBehaviorColor(parsed.behavior.risk)}`}>
          <div className="insight-card-icon">📊</div>
          <div className="insight-card-content">
            <span className="insight-card-label">Spending Behavior</span>
            <span className="insight-card-value">{parsed.behavior.type}</span>
            <span className={`insight-card-badge ${getBehaviorColor(parsed.behavior.risk)}`}>
              {parsed.behavior.risk} Risk
            </span>
          </div>
        </div>

        <div className={`insight-card ${getHealthColor(parsed.health.level)}`}>
          <div className="insight-card-icon">❤️</div>
          <div className="insight-card-content">
            <span className="insight-card-label">Financial Health</span>
            <span className="insight-card-value">{parsed.health.level}</span>
            <span className="insight-card-badge neutral">Score: {parsed.health.score}</span>
          </div>
        </div>

        <div className="insight-card income-card">
          <div className="insight-card-icon">💰</div>
          <div className="insight-card-content">
            <span className="insight-card-label">Monthly Income</span>
            <span className="insight-card-value">{parsed.income}</span>
          </div>
        </div>

        <div className="insight-card budget-card">
          <div className="insight-card-icon">📋</div>
          <div className="insight-card-content">
            <span className="insight-card-label">Recommended Budget</span>
            <span className="insight-card-value">{parsed.recommendedBudget}</span>
            {parsed.wasScaled && (
              <span className="insight-card-badge warning">Adjusted to fit income</span>
            )}
          </div>
        </div>
      </div>

      {/* Budget Adjustment Alert */}
      {parsed.wasScaled && (
        <div className="budget-alert">
          <span className="alert-icon">⚠️</span>
          <div className="alert-content">
            <strong>Budget Adjusted</strong>
            <p>Your recommended budget has been scaled down to ensure total spending stays within your income limit.</p>
          </div>
        </div>
      )}

      {/* Recommendations Section */}
      <div className="recommendations-section">
        <h3>📝 Recommended Changes</h3>
        <p className="section-subtitle">Based on the 50/30/20 budgeting rule and your financial health analysis</p>

        {/* Areas to Increase */}
        {increases.length > 0 && (
          <div className="change-group increase-group">
            <h4>
              <span className="group-icon">📈</span>
              Areas to Increase
            </h4>
            <div className="change-list">
              {increases.map((change, index) => (
                <div key={index} className="change-item increase">
                  <div className="change-category">{change.category}</div>
                  <div className="change-amounts">
                    <span className="from">{change.from}</span>
                    <span className="arrow">→</span>
                    <span className="to">{change.to}</span>
                  </div>
                  <div className="change-percent positive">{change.percent}</div>
                  <div className="change-reason">{change.reason}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Areas to Reduce */}
        {decreases.length > 0 && (
          <div className="change-group decrease-group">
            <h4>
              <span className="group-icon">📉</span>
              Areas to Reduce
            </h4>
            <div className="change-list">
              {decreases.map((change, index) => (
                <div key={index} className="change-item decrease">
                  <div className="change-category">{change.category}</div>
                  <div className="change-amounts">
                    <span className="from">{change.from}</span>
                    <span className="arrow">→</span>
                    <span className="to">{change.to}</span>
                  </div>
                  <div className="change-percent negative">{change.percent}</div>
                  <div className="change-reason">{change.reason}</div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Notes */}
      {parsed.notes.length > 0 && (
        <div className="notes-section">
          <h4>⚡ Important Notes</h4>
          <ul>
            {parsed.notes.map((note, index) => (
              <li key={index}>{note}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Closing */}
      <div className="action-footer">
        <div className="tip-box">
          <span className="tip-icon">💡</span>
          <span className="tip-text">
            {parsed.closing || 'Review these recommendations regularly and adjust based on your changing financial goals.'}
          </span>
        </div>
      </div>
    </div>
  );
};

export default RecommendationText;
