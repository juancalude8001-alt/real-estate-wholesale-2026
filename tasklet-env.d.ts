/* ============================================================
   ENHANCED REAL ESTATE DASHBOARD STYLES
   ============================================================ */

:root {
  --primary: #2563eb;
  --success: #10b981;
  --warning: #f59e0b;
  --danger: #ef4444;
  --dark: #1f2937;
  --light: #f9fafb;
  --border: #e5e7eb;
  --text: #374151;
  --text-light: #6b7280;
  --gold: #d97706;
  --silver: #8b5cf6;
  --bronze: #f97316;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
  padding: 1rem;
}

/* ============================================================
   DASHBOARD CONTAINER
   ============================================================ */

.dashboard-container {
  max-width: 1600px;
  margin: 0 auto;
}

.dashboard-header {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  margin-bottom: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.dashboard-header h1 {
  font-size: 2rem;
  color: var(--dark);
  margin-bottom: 0.5rem;
}

.dashboard-header p {
  color: var(--text-light);
  font-size: 1rem;
}

.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 400px;
  background: white;
  border-radius: 12px;
  font-size: 1.1rem;
  color: var(--text-light);
}

/* ============================================================
   DASHBOARD LAYOUT (2-COLUMN)
   ============================================================ */

.dashboard-layout {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 1.5rem;
}

@media (max-width: 1200px) {
  .dashboard-layout {
    grid-template-columns: 1fr;
  }
}

/* ============================================================
   LEFT PANEL: DEALS LIST
   ============================================================ */

.deals-panel {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.filter-controls {
  padding: 1.5rem;
  border-bottom: 1px solid var(--border);
}

.filter-controls h3 {
  color: var(--dark);
  margin-bottom: 1rem;
}

.filter-buttons {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.filter-btn {
  padding: 0.5rem 1rem;
  border: 2px solid var(--border);
  background: white;
  color: var(--text);
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.filter-btn:hover {
  border-color: var(--primary);
  color: var(--primary);
}

.filter-btn.active {
  background: var(--primary);
  border-color: var(--primary);
  color: white;
}

.deals-list {
  flex: 1;
  overflow-y: auto;
  padding: 0;
  max-height: calc(100vh - 300px);
}

.deal-card {
  padding: 1rem;
  border-bottom: 1px solid var(--border);
  cursor: pointer;
  transition: all 0.3s ease;
}

.deal-card:hover {
  background: var(--light);
}

.deal-card.selected {
  background: linear-gradient(135deg, rgba(37, 99, 235, 0.1), rgba(59, 130, 246, 0.1));
  border-left: 4px solid var(--primary);
  padding-left: calc(1rem - 4px);
}

.deal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.tier-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: bold;
  color: white;
}

.tier-badge.gold {
  background: var(--gold);
}

.tier-badge.silver {
  background: var(--silver);
}

.tier-badge.bronze {
  background: var(--bronze);
}

.deal-score {
  font-size: 0.9rem;
  color: var(--gold);
}

.deal-address {
  font-weight: 600;
  color: var(--dark);
  margin-bottom: 0.25rem;
}

.deal-city {
  font-size: 0.85rem;
  color: var(--text-light);
  margin-bottom: 0.75rem;
}

.deal-metrics {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.metric {
  display: flex;
  justify-content: space-between;
  font-size: 0.85rem;
}

.metric .label {
  color: var(--text-light);
}

.metric .value {
  font-weight: 600;
  color: var(--dark);
}

.status-badge {
  display: inline-block;
  padding: 0.35rem 0.75rem;
  background: var(--light);
  border: 1px solid var(--border);
  border-radius: 6px;
  font-size: 0.8rem;
  color: var(--text);
}

/* ============================================================
   RIGHT PANEL: DEAL DETAILS
   ============================================================ */

.detail-panel {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.detail-header {
  padding: 1.5rem;
  border-bottom: 2px solid var(--border);
}

.detail-header h2 {
  color: var(--dark);
  margin-bottom: 0.25rem;
}

.detail-header p {
  color: var(--text-light);
  font-size: 0.95rem;
}

/* ============================================================
   TAB NAVIGATION
   ============================================================ */

.tab-navigation {
  display: flex;
  gap: 0;
  border-bottom: 1px solid var(--border);
  overflow-x: auto;
  padding: 0 1.5rem;
  background: var(--light);
}

.tab-btn {
  padding: 1rem 1.25rem;
  border: none;
  background: transparent;
  color: var(--text-light);
  cursor: pointer;
  font-weight: 500;
  border-bottom: 3px solid transparent;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.tab-btn:hover {
  color: var(--primary);
}

.tab-btn.active {
  color: var(--primary);
  border-bottom-color: var(--primary);
}

/* ============================================================
   TAB CONTENT
   ============================================================ */

.tab-content {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
}

/* OVERVIEW TAB */

.overview-section {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}

.metric-card {
  background: var(--light);
  padding: 1rem;
  border-radius: 8px;
  border: 1px solid var(--border);
  text-align: center;
}

.metric-card.highlight {
  background: linear-gradient(135deg, rgba(37, 99, 235, 0.1), rgba(59, 130, 246, 0.1));
  border: 2px solid var(--primary);
}

.metric-card .label {
  display: block;
  color: var(--text-light);
  font-size: 0.85rem;
  margin-bottom: 0.5rem;
}

.metric-card .value {
  display: block;
  color: var(--dark);
  font-size: 1.3rem;
  font-weight: bold;
}

.property-info,
.seller-info {
  background: var(--light);
  padding: 1.5rem;
  border-radius: 8px;
  border: 1px solid var(--border);
}

.property-info h4,
.seller-info h4 {
  color: var(--dark);
  margin-bottom: 1rem;
  font-size: 1rem;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.info-item {
  display: flex;
  flex-direction: column;
}

.info-item .label {
  color: var(--text-light);
  font-size: 0.85rem;
  margin-bottom: 0.25rem;
  font-weight: 500;
}

.info-item span:last-child {
  color: var(--dark);
  font-weight: 500;
}

/* VOICE TAB */

.voice-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.voice-status {
  background: var(--light);
  padding: 1.5rem;
  border-radius: 8px;
  border: 1px solid var(--border);
}

.voice-status h4 {
  color: var(--dark);
  margin-bottom: 1rem;
}

.status-indicator {
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--primary);
  padding: 1rem;
  background: white;
  border: 2px solid var(--primary);
  border-radius: 6px;
  text-align: center;
}

.voice-history {
  background: var(--light);
  padding: 1.5rem;
  border-radius: 8px;
  border: 1px solid var(--border);
}

.voice-history h4 {
  color: var(--dark);
  margin-bottom: 1rem;
}

/* OFFERS TAB */

.offers-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.no-offers {
  text-align: center;
  padding: 2rem;
  background: var(--light);
  border-radius: 8px;
  border: 2px dashed var(--border);
}

.no-offers p {
  color: var(--text-light);
  margin-bottom: 1rem;
}

.offers-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.offer-card {
  padding: 1.5rem;
  border-radius: 8px;
  border: 2px solid var(--border);
  background: white;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.offer-card.aggressive {
  border-color: var(--danger);
  background: rgba(239, 68, 68, 0.05);
}

.offer-card.balanced {
  border-color: var(--warning);
  background: rgba(245, 158, 11, 0.05);
}

.offer-card.conservative {
  border-color: var(--success);
  background: rgba(16, 185, 129, 0.05);
}

.offer-tier {
  font-weight: bold;
  font-size: 0.9rem;
}

.offer-card.aggressive .offer-tier {
  color: var(--danger);
}

.offer-card.balanced .offer-tier {
  color: var(--warning);
}

.offer-card.conservative .offer-tier {
  color: var(--success);
}

.offer-price {
  font-size: 2rem;
  font-weight: bold;
  color: var(--dark);
}

.offer-metrics {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.75rem;
}

.offer-metrics .metric {
  flex-direction: column;
  text-align: center;
}

.offer-metrics .label {
  color: var(--text-light);
  font-size: 0.8rem;
  margin-bottom: 0.25rem;
}

.offer-metrics .value {
  color: var(--dark);
  font-weight: bold;
}

.offer-terms {
  background: var(--light);
  padding: 1rem;
  border-radius: 6px;
}

.offer-terms strong {
  display: block;
  color: var(--dark);
  margin-bottom: 0.5rem;
}

.offer-terms ul {
  list-style: none;
  padding: 0;
}

.offer-terms li {
  color: var(--text);
  font-size: 0.9rem;
  margin-bottom: 0.25rem;
}

.offer-status {
  font-size: 0.9rem;
  color: var(--text-light);
  padding: 0.75rem;
  background: var(--light);
  border-radius: 6px;
}

.offer-actions {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

/* CONTRACT TAB */

.contract-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.no-contracts {
  text-align: center;
  padding: 2rem;
  background: var(--light);
  border-radius: 8px;
  border: 2px dashed var(--border);
}

.no-contracts p {
  color: var(--text);
  margin-bottom: 0.5rem;
}

.contracts-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.contract-card {
  padding: 1.5rem;
  border: 2px solid var(--primary);
  border-radius: 8px;
  background: rgba(37, 99, 235, 0.05);
}

.contract-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.contract-type {
  font-weight: bold;
  color: var(--primary);
}

.contract-status {
  display: inline-block;
  padding: 0.35rem 0.75rem;
  background: var(--primary);
  color: white;
  border-radius: 6px;
  font-size: 0.8rem;
}

.contract-meta {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border);
}

.meta-item {
  display: flex;
  flex-direction: column;
}

.meta-item .label {
  color: var(--text-light);
  font-size: 0.85rem;
  margin-bottom: 0.25rem;
}

.contract-actions {
  display: flex;
  gap: 0.75rem;
}

/* STATUS TAB */

.status-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.status-detail {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.status-detail h4 {
  color: var(--dark);
  font-size: 1rem;
  margin-top: 0.5rem;
}

.stage-indicator {
  background: linear-gradient(135deg, rgba(37, 99, 235, 0.1), rgba(59, 130, 246, 0.1));
  padding: 1.5rem;
  border-radius: 8px;
  border: 2px solid var(--primary);
  text-align: center;
}

.stage-name {
  font-size: 1.3rem;
  font-weight: bold;
  color: var(--primary);
}

.status-detail p {
  color: var(--text);
  line-height: 1.6;
}

.no-status {
  text-align: center;
  padding: 2rem;
  background: var(--light);
  border-radius: 8px;
  border: 1px solid var(--border);
  color: var(--text-light);
}

.deal-pipeline {
  background: var(--light);
  padding: 1.5rem;
  border-radius: 8px;
  border: 1px solid var(--border);
}

.deal-pipeline h4 {
  color: var(--dark);
  margin-bottom: 1.5rem;
}

.pipeline-stages {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  gap: 0.75rem;
}

.pipeline-stage {
  padding: 0.75rem;
  background: white;
  border: 2px solid var(--border);
  border-radius: 6px;
  text-align: center;
  font-size: 0.85rem;
  font-weight: 500;
  color: var(--text-light);
  transition: all 0.3s ease;
}

.pipeline-stage.active {
  background: linear-gradient(135deg, rgba(37, 99, 235, 0.2), rgba(59, 130, 246, 0.2));
  border-color: var(--primary);
  color: var(--primary);
  transform: scale(1.05);
}

/* ============================================================
   BUTTONS
   ============================================================ */

.btn-primary,
.btn-secondary {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.95rem;
}

.btn-primary {
  background: var(--primary);
  color: white;
}

.btn-primary:hover {
  background: #1d4ed8;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
}

.btn-primary:active {
  transform: translateY(0);
}

.btn-secondary {
  background: var(--light);
  color: var(--primary);
  border: 2px solid var(--primary);
}

.btn-secondary:hover {
  background: var(--primary);
  color: white;
}

/* ============================================================
   SCROLLBAR STYLING
   ============================================================ */

::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: var(--light);
}

::-webkit-scrollbar-thumb {
  background: var(--border);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #d1d5db;
}

/* ============================================================
   RESPONSIVE
   ============================================================ */

@media (max-width: 768px) {
  .dashboard-header {
    padding: 1rem;
  }

  .dashboard-header h1 {
    font-size: 1.5rem;
  }

  .filter-buttons {
    flex-direction: column;
  }

  .filter-btn {
    width: 100%;
  }

  .metrics-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .offers-grid {
    grid-template-columns: 1fr;
  }

  .tab-navigation {
    padding: 0;
  }

  .tab-btn {
    flex: 1;
    padding: 0.75rem;
    font-size: 0.85rem;
  }

  .deal-pipeline {
    padding: 1rem;
  }

  .pipeline-stages {
    grid-template-columns: repeat(2, 1fr);
  }
}
