import React, { useState, useEffect } from 'react';
import { createRoot } from 'react-dom/client';
import './styles.css';

interface Deal {
  id: string;
  address: string;
  city: string;
  property_type: string;
  opening_bid: number;
  arv_estimate: number;
  repair_estimate: number;
  mao: number;
  estimated_profit: number;
  deal_score: number;
  deal_tier: string;
  discount_from_arv_percent: number;
  time_remaining_days: number;
  auction_date: string;
  bedrooms: number;
  bathrooms: number;
  square_feet: number;
  year_built: number;
  photo_count: number;
  owner_name?: string;
  phone_number?: string;
}

interface CallOutcome {
  call_id: string;
  timestamp: string;
  motivation_level: string;
  is_interested: boolean;
  price_expectation?: number;
  notes: string;
}

export const App: React.FC = () => {
  return <RealEstateDashboard />;
};

function RealEstateDashboard() {
  const [deals, setDeals] = useState<Deal[]>([]);
  const [selectedDeal, setSelectedDeal] = useState<Deal | null>(null);
  const [filter, setFilter] = useState<'all' | 'gold' | 'silver' | 'bronze'>('all');
  const [loading, setLoading] = useState(true);
  const [sortBy, setSortBy] = useState<'profit' | 'score' | 'discount'>('profit');
  const [approvedDeals, setApprovedDeals] = useState<Set<string>>(new Set());
  const [callHistory, setCallHistory] = useState<Map<string, CallOutcome[]>>(new Map());
  const [callInProgress, setCallInProgress] = useState<string | null>(null);
  const [showCallForm, setShowCallForm] = useState(false);
  const [selectedDealForCall, setSelectedDealForCall] = useState<Deal | null>(null);
  const [voiceStats, setVoiceStats] = useState<any>(null);

  useEffect(() => {
    loadDeals();
    loadVoiceStats();
  }, []);

  const loadDeals = async () => {
    try {
      const response = await fetch('/api/deals');
      if (response.ok) {
        const data = await response.json();
        if (data && Array.isArray(data)) {
          setDeals(data);
        } else {
          setDeals(sampleDeals);
        }
      } else {
        setDeals(sampleDeals);
      }
    } catch (error) {
      console.error('Error loading deals:', error);
      // Use static sample data
      setDeals(sampleDeals);
    } finally {
      setLoading(false);
    }
  };

  const getDealTier = (score: number): string => {
    if (score >= 80) return 'gold';
    if (score >= 60) return 'silver';
    if (score >= 40) return 'bronze';
    return 'rejected';
  };

  const loadVoiceStats = async () => {
    try {
      const response = await fetch('/api/calls/stats');
      if (response.ok) {
        const stats = await response.json();
        setVoiceStats(stats);
      }
    } catch (error) {
      console.error('Error loading voice stats:', error);
    }
  };

  const loadCallHistory = async (dealId: string) => {
    try {
      const response = await fetch(`/api/calls/deal/${dealId}/history`);
      if (response.ok) {
        const data = await response.json();
        const newHistory = new Map(callHistory);
        newHistory.set(dealId, data.calls);
        setCallHistory(newHistory);
      }
    } catch (error) {
      console.error('Error loading call history:', error);
    }
  };

  const initiateCall = async (deal: Deal) => {
    if (!deal.owner_name || !deal.phone_number) {
      alert('Owner name and phone number required to make a call');
      return;
    }

    setCallInProgress(deal.id);
    setSelectedDealForCall(deal);

    try {
      const response = await fetch('/api/calls/initiate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          deal_id: deal.id,
          owner_name: deal.owner_name,
          phone_number: deal.phone_number,
          property_address: deal.address,
          arv_estimate: deal.arv_estimate,
          suggested_offer_low: deal.mao,
          suggested_offer_high: deal.mao + 20000,
          days_to_auction: deal.time_remaining_days,
          bedrooms: deal.bedrooms,
          bathrooms: deal.bathrooms,
          square_feet: deal.square_feet,
        }),
      });

      if (response.ok) {
        const result = await response.json();
        alert(`Call initiated to ${deal.owner_name}!\nCallID: ${result.call_id}`);
        loadCallHistory(deal.id);
        setShowCallForm(true);
      } else {
        alert('Failed to initiate call');
        setCallInProgress(null);
      }
    } catch (error) {
      alert(`Error: ${error}`);
      setCallInProgress(null);
    }
  };

  const filteredDeals = deals
    .filter(deal => filter === 'all' || deal.deal_tier === filter)
    .sort((a, b) => {
      if (sortBy === 'profit') return b.estimated_profit - a.estimated_profit;
      if (sortBy === 'score') return b.deal_score - a.deal_score;
      if (sortBy === 'discount') return b.discount_from_arv_percent - a.discount_from_arv_percent;
      return 0;
    });

  const handleApprove = (dealId: string) => {
    const newApproved = new Set(approvedDeals);
    if (newApproved.has(dealId)) {
      newApproved.delete(dealId);
    } else {
      newApproved.add(dealId);
    }
    setApprovedDeals(newApproved);
  };

  const stats = {
    totalDeals: deals.length,
    goldTier: deals.filter(d => d.deal_tier === 'gold').length,
    silverTier: deals.filter(d => d.deal_tier === 'silver').length,
    totalProfit: deals.reduce((sum, d) => sum + d.estimated_profit, 0),
    approvedCount: approvedDeals.size,
  };

  return (
    <div className="dashboard">
      {/* Header */}
      <div className="header">
        <h1>🏠 Real Estate Wholesale System</h1>
        <p>Automated Deal Analysis & Approval Pipeline</p>
      </div>

      {/* Stats Dashboard */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-label">Properties Found</div>
          <div className="stat-value">{stats.totalDeals}</div>
        </div>
        <div className="stat-card gold">
          <div className="stat-label">Gold Tier Deals</div>
          <div className="stat-value">{stats.goldTier}</div>
        </div>
        <div className="stat-card silver">
          <div className="stat-label">Silver Tier Deals</div>
          <div className="stat-value">{stats.silverTier}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Total Profit Potential</div>
          <div className="stat-value">${(stats.totalProfit / 1000).toFixed(1)}K</div>
        </div>
        <div className="stat-card highlight">
          <div className="stat-label">Approved for Outreach</div>
          <div className="stat-value">{stats.approvedCount}/{stats.totalDeals}</div>
        </div>
      </div>

      {/* Controls */}
      <div className="controls">
        <div className="filter-group">
          <label>Filter by Tier:</label>
          <select value={filter} onChange={(e) => setFilter(e.target.value as any)}>
            <option value="all">All Deals</option>
            <option value="gold">🥇 Gold Tier (80+)</option>
            <option value="silver">🥈 Silver Tier (60-79)</option>
            <option value="bronze">🥉 Bronze Tier (40-59)</option>
          </select>
        </div>

        <div className="filter-group">
          <label>Sort by:</label>
          <select value={sortBy} onChange={(e) => setSortBy(e.target.value as any)}>
            <option value="profit">Highest Profit</option>
            <option value="score">Highest Score</option>
            <option value="discount">Biggest Discount</option>
          </select>
        </div>

        <div className="filter-group">
          <button className="btn-primary" onClick={loadDeals}>🔄 Refresh Data</button>
        </div>
      </div>

      {/* Deals List */}
      <div className="deals-container">
        <div className="deals-list">
          <div className="list-header">
            <span>Address</span>
            <span>City</span>
            <span>Score</span>
            <span>Profit</span>
            <span>Action</span>
          </div>

          {filteredDeals.map(deal => (
            <div 
              key={deal.id} 
              className={`deal-item ${selectedDeal?.id === deal.id ? 'selected' : ''} ${approvedDeals.has(deal.id) ? 'approved' : ''}`}
              onClick={() => setSelectedDeal(deal)}
            >
              <span className="deal-address">{deal.address}</span>
              <span className="deal-city">{deal.city}</span>
              <span className="deal-score">
                <span className={`badge tier-${deal.deal_tier}`}>{deal.deal_score}</span>
              </span>
              <span className="deal-profit">${(deal.estimated_profit / 1000).toFixed(1)}K</span>
              <button
                className={`btn-approve ${approvedDeals.has(deal.id) ? 'approved' : ''}`}
                onClick={(e) => {
                  e.stopPropagation();
                  handleApprove(deal.id);
                }}
              >
                {approvedDeals.has(deal.id) ? '✓ Approved' : 'Approve'}
              </button>
            </div>
          ))}
        </div>

        {/* Deal Details Panel */}
        {selectedDeal && (
          <div className="deal-details">
            <h2>{selectedDeal.address}</h2>
            <div className="detail-divider"></div>

            <div className="detail-section">
              <h3>📍 Property Information</h3>
              <div className="detail-grid">
                <div className="detail-item">
                  <span className="label">Address:</span>
                  <span className="value">{selectedDeal.address}, {selectedDeal.city}</span>
                </div>
                <div className="detail-item">
                  <span className="label">Property Type:</span>
                  <span className="value">{selectedDeal.property_type}</span>
                </div>
                <div className="detail-item">
                  <span className="label">Bedrooms:</span>
                  <span className="value">{selectedDeal.bedrooms || 'N/A'}</span>
                </div>
                <div className="detail-item">
                  <span className="label">Bathrooms:</span>
                  <span className="value">{selectedDeal.bathrooms || 'N/A'}</span>
                </div>
                <div className="detail-item">
                  <span className="label">Square Feet:</span>
                  <span className="value">{selectedDeal.square_feet?.toLocaleString() || 'N/A'}</span>
                </div>
                <div className="detail-item">
                  <span className="label">Year Built:</span>
                  <span className="value">{selectedDeal.year_built || 'N/A'}</span>
                </div>
              </div>
            </div>

            <div className="detail-section">
              <h3>💰 Financial Analysis</h3>
              <div className="detail-grid">
                <div className="detail-item">
                  <span className="label">Opening Bid:</span>
                  <span className="value">${selectedDeal.opening_bid?.toLocaleString() || 'N/A'}</span>
                </div>
                <div className="detail-item">
                  <span className="label">ARV Estimate:</span>
                  <span className="value">${selectedDeal.arv_estimate?.toLocaleString() || 'N/A'}</span>
                </div>
                <div className="detail-item">
                  <span className="label">Estimated Repairs:</span>
                  <span className="value">${selectedDeal.repair_estimate?.toLocaleString() || 'N/A'}</span>
                </div>
                <div className="detail-item">
                  <span className="label">Max Allowable Offer:</span>
                  <span className="value highlight">${selectedDeal.mao?.toLocaleString() || 'N/A'}</span>
                </div>
                <div className="detail-item big">
                  <span className="label">💎 Estimated Profit:</span>
                  <span className="value profit">${selectedDeal.estimated_profit?.toLocaleString() || 'N/A'}</span>
                </div>
                <div className="detail-item">
                  <span className="label">Discount from ARV:</span>
                  <span className="value">{selectedDeal.discount_from_arv_percent?.toFixed(1) || 'N/A'}%</span>
                </div>
              </div>
            </div>

            <div className="detail-section">
              <h3>🎯 Deal Scoring</h3>
              <div className="score-display">
                <div className={`score-circle tier-${selectedDeal.deal_tier}`}>
                  <span className="score-number">{selectedDeal.deal_score}</span>
                  <span className="score-max">/ 100</span>
                </div>
                <div className="score-info">
                  <p className={`tier-badge tier-${selectedDeal.deal_tier}`}>
                    {selectedDeal.deal_tier === 'gold' && '🥇 GOLD TIER - Premium Deal'}
                    {selectedDeal.deal_tier === 'silver' && '🥈 SILVER TIER - Good Deal'}
                    {selectedDeal.deal_tier === 'bronze' && '🥉 BRONZE TIER - Fair Deal'}
                    {selectedDeal.deal_tier === 'rejected' && '❌ Below Threshold'}
                  </p>
                  <p className="tier-description">
                    {selectedDeal.deal_tier === 'gold' && 'Excellent profit potential with strong discount and timeline'}
                    {selectedDeal.deal_tier === 'silver' && 'Good deal with solid profit potential'}
                    {selectedDeal.deal_tier === 'bronze' && 'Fair deal, requires careful negotiation'}
                  </p>
                </div>
              </div>
            </div>

            <div className="detail-section">
              <h3>⏰ Auction Details</h3>
              <div className="detail-grid">
                <div className="detail-item">
                  <span className="label">Auction Date:</span>
                  <span className="value">{selectedDeal.auction_date || 'N/A'}</span>
                </div>
                <div className="detail-item">
                  <span className="label">Days Remaining:</span>
                  <span className="value">{selectedDeal.time_remaining_days || 'N/A'} days</span>
                </div>
                <div className="detail-item">
                  <span className="label">Photos Available:</span>
                  <span className="value">{selectedDeal.photo_count || 'N/A'}</span>
                </div>
              </div>
            </div>

            {/* Voice Calling Section */}
            <div className="detail-section voice-section">
              <h3>📞 Voice Outreach</h3>
              <div className="voice-card">
                <p className="voice-description">
                  Call the property owner to qualify the deal and discover their motivation.
                </p>
                <div className="voice-buttons">
                  <button
                    className={`btn-call-large ${callInProgress === selectedDeal.id ? 'loading' : ''}`}
                    onClick={() => initiateCall(selectedDeal)}
                    disabled={callInProgress === selectedDeal.id}
                  >
                    {callInProgress === selectedDeal.id ? '📞 Call in Progress...' : '📞 Call Owner Now'}
                  </button>
                  <button
                    className="btn-secondary"
                    onClick={() => loadCallHistory(selectedDeal.id)}
                  >
                    📋 View Call History
                  </button>
                </div>
                
                {callHistory.has(selectedDeal.id) && callHistory.get(selectedDeal.id)!.length > 0 && (
                  <div className="call-history">
                    <h4>Call History:</h4>
                    {callHistory.get(selectedDeal.id)!.map((call, idx) => (
                      <div key={idx} className="history-item">
                        <span className="call-date">{new Date(call.timestamp).toLocaleDateString()}</span>
                        <span className={`motivation-badge motivation-${call.motivation_level}`}>
                          {call.motivation_level}
                        </span>
                        <span className="call-status">
                          {call.is_interested ? '✓ Interested' : '✗ Not Interested'}
                        </span>
                        {call.price_expectation && (
                          <span className="call-price">${call.price_expectation.toLocaleString()}</span>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>

            <div className="approval-section">
              <button
                className={`btn-approve-large ${approvedDeals.has(selectedDeal.id) ? 'approved' : ''}`}
                onClick={() => handleApprove(selectedDeal.id)}
              >
                {approvedDeals.has(selectedDeal.id) ? '✓ Approved - Ready for Outreach' : '✓ Approve This Deal'}
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Summary */}
      <div className="summary-section">
        <div className="summary-box">
          <h3>📊 Pipeline Summary</h3>
          <p>Total Properties Analyzed: <strong>{stats.totalDeals}</strong></p>
          <p>Deals Approved for Outreach: <strong>{stats.approvedCount}</strong></p>
          <p>Total Profit Potential: <strong>${(stats.totalProfit / 1000).toFixed(1)}K</strong></p>
          <p className="note">✓ Next Step: Generate offers and call scripts for approved deals</p>
        </div>
      </div>
    </div>
  );
}

// Sample deals for fallback
const sampleDeals: Deal[] = [
  {
    id: '1',
    address: '4702 Elm Street',
    city: 'Dallas',
    property_type: 'single-family',
    opening_bid: 135000,
    arv_estimate: 195750,
    repair_estimate: 50000,
    mao: 86775,
    estimated_profit: 75304,
    deal_score: 75,
    deal_tier: 'silver',
    discount_from_arv_percent: 30.9,
    time_remaining_days: 17,
    auction_date: 'Soon',
    bedrooms: 5,
    bathrooms: 3,
    square_feet: 2800,
    year_built: 2010,
    photo_count: 20,
  },
  {
    id: '2',
    address: '621 Enterprise Boulevard',
    city: 'Arlington',
    property_type: 'multi-family',
    opening_bid: 125000,
    arv_estimate: 187500,
    repair_estimate: 50000,
    mao: 81250,
    estimated_profit: 66938,
    deal_score: 68,
    deal_tier: 'silver',
    discount_from_arv_percent: 33.3,
    time_remaining_days: 25,
    auction_date: 'Soon',
    bedrooms: 6,
    bathrooms: 3,
    square_feet: 3200,
    year_built: 2001,
    photo_count: 18,
  },
];

// Mount React app
createRoot(document.getElementById('root')!).render(<App />);
