import React from 'react';
import { BehaviorInsight as BehaviorInsightType, FinancialInsight as FinancialInsightType } from '../../types';
import './InsightCards.css';

interface InsightCardsProps {
  behaviorInsight: BehaviorInsightType;
  financialInsight: FinancialInsightType;
}

const getRiskColor = (risk: string): string => {
  switch (risk) {
    case 'Low': return '#98DDCA';
    case 'Medium': return '#FFD3D5';
    case 'High': return '#F5AFAF';
    default: return '#E2E8F0';
  }
};

const getHealthColor = (health: string): string => {
  switch (health) {
    case 'Excellent': return '#98DDCA';
    case 'Good': return '#BEE4D0';
    case 'Fair': return '#FFD3D5';
    case 'Poor': return '#F5AFAF';
    default: return '#E2E8F0';
  }
};

const getScoreGradient = (score: number): string => {
  if (score >= 80) return 'linear-gradient(135deg, #98DDCA 0%, #B9F3E4 100%)';
  if (score >= 60) return 'linear-gradient(135deg, #BEE4D0 0%, #D2F5E3 100%)';
  if (score >= 40) return 'linear-gradient(135deg, #FFD3D5 0%, #FFCDC9 100%)';
  return 'linear-gradient(135deg, #F5AFAF 0%, #FDACAC 100%)';
};

const InsightCards: React.FC<InsightCardsProps> = ({ behaviorInsight, financialInsight }) => {
  return (
    <div className="insight-cards">
      <div className="section-header">
        <h2>🔍 Behavior & Financial Insight</h2>
      </div>

      <div className="insights-container">
        {/* Behavior Insight Card */}
        <div className="insight-card behavior-card">
          <div className="card-header">
            <span className="card-icon">🧠</span>
            <h3>Behavior Insight</h3>
          </div>
          
          <div className="insight-content">
            <div className="insight-row">
              <span className="label">Type</span>
              <span className="value type-badge">{behaviorInsight.type}</span>
            </div>
            
            <div className="insight-row">
              <span className="label">Risk Level</span>
              <span 
                className="value risk-badge"
                style={{ backgroundColor: getRiskColor(behaviorInsight.riskLevel) }}
              >
                {behaviorInsight.riskLevel}
              </span>
            </div>
            
            <div className="insight-description">
              <p>{behaviorInsight.description}</p>
            </div>
          </div>
        </div>

        {/* Financial Insight Card */}
        <div className="insight-card financial-card">
          <div className="card-header">
            <span className="card-icon">📊</span>
            <h3>Financial Insight</h3>
          </div>
          
          <div className="insight-content">
            <div className="health-score-circle" style={{ background: getScoreGradient(financialInsight.healthScore) }}>
              <span className="score-value">{financialInsight.healthScore}</span>
              <span className="score-label">Health Score</span>
            </div>
            
            <div className="financial-metrics">
              <div className="insight-row">
                <span className="label">Health Level</span>
                <span 
                  className="value health-badge"
                  style={{ backgroundColor: getHealthColor(financialInsight.healthLevel) }}
                >
                  {financialInsight.healthLevel}
                </span>
              </div>
              
              <div className="insight-row">
                <span className="label">Risk Level</span>
                <span 
                  className="value risk-badge"
                  style={{ backgroundColor: getRiskColor(financialInsight.riskLevel) }}
                >
                  {financialInsight.riskLevel}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default InsightCards;
