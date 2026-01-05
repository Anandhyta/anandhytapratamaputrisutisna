import React from 'react';
import './RecommendationText.css';

interface RecommendationTextProps {
  text: string;
}

const RecommendationText: React.FC<RecommendationTextProps> = ({ text }) => {
  // Parse markdown-like text with **bold** markers
  const formatText = (content: string) => {
    const parts = content.split(/(\*\*[^*]+\*\*)/g);
    return parts.map((part, index) => {
      if (part.startsWith('**') && part.endsWith('**')) {
        return <strong key={index}>{part.slice(2, -2)}</strong>;
      }
      return part;
    });
  };

  // Split text into paragraphs
  const paragraphs = text.split('\n\n').filter(p => p.trim());

  return (
    <div className="recommendation-text">
      <div className="section-header">
        <h2>💡 Personalized Recommendations</h2>
        <button className="export-btn" title="Export as PDF (UI only)">
          <span className="export-icon">📄</span>
          Export PDF
        </button>
      </div>

      <div className="text-content">
        {paragraphs.map((paragraph, index) => (
          <p key={index}>{formatText(paragraph)}</p>
        ))}
      </div>

      <div className="action-footer">
        <div className="tip-box">
          <span className="tip-icon">💡</span>
          <span className="tip-text">
            Review these recommendations regularly and adjust based on your changing financial goals.
          </span>
        </div>
      </div>
    </div>
  );
};

export default RecommendationText;
