import React, { useState } from 'react';
import CurrentExpenses from '../CurrentExpenses';
import InsightCards from '../InsightCards';
import RecommendedBudget from '../RecommendedBudget';
import RecommendationText from '../RecommendationText';
import { UserInsight } from '../../types';
import { fetchUserInsight } from '../../data/mockData';
import './Dashboard.css';

type TabType = 'expenses' | 'insights' | 'budget' | 'recommendations';

const Dashboard: React.FC = () => {
  const [userId, setUserId] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [userInsight, setUserInsight] = useState<UserInsight | null>(null);
  const [activeTab, setActiveTab] = useState<TabType>('expenses');

  const handleAnalyze = async () => {
    if (!userId.trim()) {
      setError('Please enter a valid User ID');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const result = await fetchUserInsight(userId);
      if (result) {
        setUserInsight(result);
        setActiveTab('expenses');
      } else {
        setError('User not found. Please check the User ID and try again.');
      }
    } catch (err) {
      setError('An error occurred while fetching data. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleAnalyze();
    }
  };

  const tabs: { id: TabType; label: string; icon: string }[] = [
    { id: 'expenses', label: 'Current Expenses', icon: '💳' },
    { id: 'insights', label: 'Behavior & Financial Insight', icon: '🔍' },
    { id: 'budget', label: 'Recommended Budget', icon: '📋' },
    { id: 'recommendations', label: 'Recommendations', icon: '💡' },
  ];

  const handleGoHome = () => {
    setUserInsight(null);
    setUserId('');
    setError(null);
    setActiveTab('expenses');
  };

  return (
    <div className="dashboard">
      {/* Logo Navbar */}
      <nav className="logo-navbar">
        <div className="logo-container">
          <button className="logo" onClick={handleGoHome} title="Go to Home">
            <div className="logo-icon">
              <span className="logo-coin">💰</span>
              <span className="logo-chart">📊</span>
              <div className="logo-circle"></div>
            </div>
            <span className="logo-text">FineSight</span>
          </button>
        </div>
      </nav>

      {/* Header Section */}
      <header className="dashboard-header">
        <div className="header-content">
          <div className="title-wrapper">
            <span className="sparkle sparkle-1">✨</span>
            <h1>
              <span className="title-line-1">Personal Financial</span>
              <span className="title-line-2">Insight Dashboard</span>
            </h1>
            <span className="sparkle sparkle-2">💎</span>
          </div>
          <p className="subtitle">
            Your money, your story 💕 Let us help you <span className="highlight">spend smarter</span>, 
            <span className="highlight">save better</span>, and <span className="highlight">grow faster</span>!
          </p>
          <div className="header-badges">
            <span className="badge">🎯 Smart Analysis</span>
            <span className="badge">📊 Data-Driven</span>
            <span className="badge">💡 Personalized</span>
          </div>
        </div>
      </header>

      {/* Input Section */}
      <section className="input-section">
        <div className="input-card">
          <div className="input-group">
            <label htmlFor="userId">User ID</label>
            <div className="input-wrapper">
              <input
                type="text"
                id="userId"
                placeholder="e.g., 16"
                value={userId}
                onChange={(e) => setUserId(e.target.value)}
                onKeyPress={handleKeyPress}
                disabled={loading}
              />
              <button 
                className="analyze-btn" 
                onClick={handleAnalyze}
                disabled={loading}
              >
                {loading ? (
                  <>
                    <span className="spinner"></span>
                    Analyzing...
                  </>
                ) : (
                  <>
                    <span className="btn-icon">🔍</span>
                    Analyze
                  </>
                )}
              </button>
            </div>
          </div>

          {error && (
            <div className="error-message">
              <span className="error-icon">⚠️</span>
              {error}
            </div>
          )}
        </div>
      </section>

      {/* Results Section */}
      {userInsight && (
        <section className="results-section">
          {/* User Info Banner */}
          <div className="user-banner">
            <div className="user-avatar">
              <div className="person-icon">
                <div className="person-head"></div>
                <div className="person-body"></div>
              </div>
            </div>
            <div className="user-info">
              <h2>User ID: {userInsight.userId}</h2>
            </div>
          </div>

          {/* Tabs Navigation */}
          <nav className="tabs-nav">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                className={`tab-btn ${activeTab === tab.id ? 'active' : ''}`}
                onClick={() => setActiveTab(tab.id)}
              >
                <span className="tab-icon">{tab.icon}</span>
                <span className="tab-label">{tab.label}</span>
              </button>
            ))}
          </nav>

          {/* Tab Content */}
          <div className="tab-content">
            {activeTab === 'expenses' && (
              <CurrentExpenses expenses={userInsight.currentExpenses} income={userInsight.income} />
            )}
            {activeTab === 'insights' && (
              <InsightCards 
                behaviorInsight={userInsight.behaviorInsight}
                financialInsight={userInsight.financialInsight}
              />
            )}
            {activeTab === 'budget' && (
              <RecommendedBudget recommendations={userInsight.budgetRecommendations} />
            )}
            {activeTab === 'recommendations' && (
              <RecommendationText text={userInsight.recommendationText} />
            )}
          </div>
        </section>
      )}

      {/* Empty State */}
      {!userInsight && !loading && (
        <section className="empty-state">
          <div className="empty-content">
            <div className="empty-icon-wrapper">
              <div className="empty-icon-circle">
                <div className="bar-chart-icon">
                  <div className="bar bar-1"></div>
                  <div className="bar bar-2"></div>
                  <div className="bar bar-3"></div>
                  <div className="bar bar-4"></div>
                </div>
                <span className="icon-float icon-1">💰</span>
                <span className="icon-float icon-2">✨</span>
                <span className="icon-float icon-3">🌟</span>
              </div>
            </div>
            <h3 className="empty-title">Let's Discover Your <span className="highlight-text">Financial Story</span> ✨</h3>
            <p>Enter your User ID above and we'll create personalized insights just for you!</p>
          </div>
        </section>
      )}

      {/* Footer */}
      <footer className="dashboard-footer">
        <p>Financial Insight Dashboard • Final Year Project © 2026</p>
      </footer>
    </div>
  );
};

export default Dashboard;
