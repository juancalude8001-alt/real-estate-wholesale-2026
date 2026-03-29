-- ============================================
-- REAL ESTATE WHOLESALE SYSTEM
-- PostgreSQL Database Schema
-- ============================================

-- Create Extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- ============================================
-- PROPERTIES TABLE (Raw Auction.com Data)
-- ============================================
CREATE TABLE IF NOT EXISTS properties (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Basic Property Info
    address VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(2) NOT NULL,
    zip_code VARCHAR(10) NOT NULL,
    county VARCHAR(100),
    
    -- Property Details
    property_type VARCHAR(50) NOT NULL, -- single-family, multi-family, land
    bedrooms INT,
    bathrooms DECIMAL(3,1),
    square_feet INT,
    lot_size DECIMAL(10,2),
    year_built INT,
    
    -- Auction Details
    opening_bid DECIMAL(12,2) NOT NULL,
    current_bid DECIMAL(12,2),
    auction_id VARCHAR(100) NOT NULL UNIQUE,
    auction_url TEXT,
    auction_date TIMESTAMP NOT NULL,
    time_remaining_days INT,
    
    -- Photos & Documentation
    photo_count INT DEFAULT 0,
    has_interior_photos BOOLEAN DEFAULT FALSE,
    has_inspection_report BOOLEAN DEFAULT FALSE,
    
    -- Data Source & Quality
    source VARCHAR(50) DEFAULT 'auction.com',
    data_verified BOOLEAN DEFAULT FALSE,
    verification_timestamp TIMESTAMP,
    
    -- Tracking
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_scraped TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Indexing
    CONSTRAINT valid_property_type CHECK (property_type IN ('single-family', 'multi-family', 'land')),
    CONSTRAINT valid_state CHECK (state IN ('TX')),
    CONSTRAINT valid_city CHECK (city IN ('Dallas', 'Fort Worth', 'Houston', 'Arlington', 'Mesquite'))
);

CREATE INDEX idx_properties_city ON properties(city);
CREATE INDEX idx_properties_property_type ON properties(property_type);
CREATE INDEX idx_properties_auction_date ON properties(auction_date);
CREATE INDEX idx_properties_opening_bid ON properties(opening_bid);
CREATE INDEX idx_properties_created_at ON properties(created_at DESC);
CREATE INDEX idx_properties_address_trgm ON properties USING gin(address gin_trgm_ops);

-- ============================================
-- ANALYSIS TABLE (Deal Analysis Results)
-- ============================================
CREATE TABLE IF NOT EXISTS analysis (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    property_id UUID NOT NULL REFERENCES properties(id) ON DELETE CASCADE,
    
    -- ARV Estimation
    arv_estimate DECIMAL(12,2) NOT NULL,
    arv_confidence INT DEFAULT 75, -- 0-100%
    arv_method VARCHAR(100), -- comp-analysis, zillow, manual
    arv_updated_at TIMESTAMP,
    
    -- Repair Estimation
    repair_category VARCHAR(50) NOT NULL, -- light, medium, heavy
    repair_estimate DECIMAL(12,2) NOT NULL,
    repair_confidence INT DEFAULT 70,
    repair_breakdown TEXT, -- JSON with roof, foundation, plumbing, etc.
    
    -- MAO & Profit
    mao DECIMAL(12,2) NOT NULL, -- Max Allowable Offer
    estimated_profit DECIMAL(12,2) NOT NULL,
    profit_margin_percent DECIMAL(5,2),
    
    -- Deal Scoring
    deal_score INT NOT NULL, -- 0-100
    deal_tier VARCHAR(20), -- gold, silver, bronze, rejected
    
    -- Discount Analysis
    discount_from_arv_percent DECIMAL(5,2),
    opening_bid_to_arv_ratio DECIMAL(4,3),
    
    -- Analysis Metadata
    analysis_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    analyst_notes TEXT,
    analyst_ai VARCHAR(100) DEFAULT 'GPT-4',
    
    UNIQUE(property_id)
);

CREATE INDEX idx_analysis_deal_score ON analysis(deal_score DESC);
CREATE INDEX idx_analysis_deal_tier ON analysis(deal_tier);
CREATE INDEX idx_analysis_estimated_profit ON analysis(estimated_profit DESC);

-- ============================================
-- APPROVALS TABLE (Human Decision Gate)
-- ============================================
CREATE TABLE IF NOT EXISTS approvals (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    property_id UUID NOT NULL REFERENCES properties(id) ON DELETE CASCADE,
    
    -- Approval Status
    analysis_approved BOOLEAN,
    approval_timestamp TIMESTAMP,
    approved_by_user VARCHAR(255),
    approval_notes TEXT,
    
    -- Decision
    ready_for_outreach BOOLEAN DEFAULT FALSE,
    rejection_reason TEXT,
    
    -- Tracking
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(property_id)
);

CREATE INDEX idx_approvals_analysis_approved ON approvals(analysis_approved);
CREATE INDEX idx_approvals_ready_for_outreach ON approvals(ready_for_outreach);

-- ============================================
-- LEADS TABLE (Owner Contact Info)
-- ============================================
CREATE TABLE IF NOT EXISTS leads (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    property_id UUID NOT NULL REFERENCES properties(id) ON DELETE CASCADE,
    
    -- Owner Info
    owner_name VARCHAR(255),
    phone_primary VARCHAR(20),
    phone_secondary VARCHAR(20),
    email VARCHAR(255),
    
    -- Contact Quality
    source VARCHAR(100), -- public-records, auction.com, reverse-lookup
    contact_found BOOLEAN DEFAULT FALSE,
    contact_quality VARCHAR(20), -- high, medium, low
    do_not_call BOOLEAN DEFAULT FALSE,
    
    -- Outreach Tracking
    first_contact_attempt TIMESTAMP,
    last_contact_attempt TIMESTAMP,
    contact_attempts INT DEFAULT 0,
    
    -- Metadata
    found_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(property_id)
);

-- ============================================
-- OFFERS TABLE (Generated Offers Per Deal)
-- ============================================
CREATE TABLE IF NOT EXISTS offers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    property_id UUID NOT NULL REFERENCES properties(id) ON DELETE CASCADE,
    
    -- Offer Details
    offer_type VARCHAR(50) NOT NULL, -- aggressive, balanced, safe
    offer_price DECIMAL(12,2) NOT NULL,
    offer_rationale TEXT,
    estimated_profit_at_offer DECIMAL(12,2),
    
    -- Offer Terms
    assignment_fee DECIMAL(12,2) DEFAULT 10000,
    closing_timeline_days INT DEFAULT 14,
    earnest_money_percent DECIMAL(5,2) DEFAULT 1.0,
    
    -- Call Script
    call_script TEXT,
    script_updated_at TIMESTAMP,
    
    -- Approval & Sending
    human_approved BOOLEAN,
    approval_timestamp TIMESTAMP,
    approved_by_user VARCHAR(255),
    
    sent_to_seller BOOLEAN DEFAULT FALSE,
    sent_timestamp TIMESTAMP,
    
    -- Response Tracking
    seller_response VARCHAR(50), -- accepted, rejected, no-answer, pending
    response_timestamp TIMESTAMP,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_offers_property_id ON offers(property_id);
CREATE INDEX idx_offers_offer_type ON offers(offer_type);
CREATE INDEX idx_offers_human_approved ON offers(human_approved);
CREATE INDEX idx_offers_sent_to_seller ON offers(sent_to_seller);

-- ============================================
-- DEALS PIPELINE TABLE (Status Tracking)
-- ============================================
CREATE TABLE IF NOT EXISTS deals_pipeline (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    property_id UUID NOT NULL REFERENCES properties(id) ON DELETE CASCADE,
    
    -- Status Tracking
    status VARCHAR(50) NOT NULL DEFAULT 'analysis',
    -- Values: analysis, approved, outreach, offer_sent, under_contract, closed, rejected
    status_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status_history TEXT, -- JSON array of status changes
    
    -- Contract Details
    contract_date TIMESTAMP,
    signed_offer_price DECIMAL(12,2),
    assignment_fee_actual DECIMAL(12,2),
    
    -- Outcome
    buyer_name VARCHAR(255),
    close_date TIMESTAMP,
    
    -- Disposition
    maxdispo_published BOOLEAN DEFAULT FALSE,
    maxdispo_link TEXT,
    
    -- Notes & Documentation
    final_notes TEXT,
    documents_attached TEXT, -- JSON array of file paths
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(property_id)
);

CREATE INDEX idx_deals_pipeline_status ON deals_pipeline(status);
CREATE INDEX idx_deals_pipeline_status_timestamp ON deals_pipeline(status_timestamp DESC);

-- ============================================
-- PROFIT TRACKING TABLE (Financial Analytics)
-- ============================================
CREATE TABLE IF NOT EXISTS profit_tracking (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    property_id UUID NOT NULL REFERENCES properties(id) ON DELETE CASCADE,
    
    -- Estimates vs Actuals
    estimated_profit DECIMAL(12,2),
    actual_profit DECIMAL(12,2),
    profit_variance DECIMAL(12,2),
    variance_percent DECIMAL(5,2),
    
    -- ROI
    roi_percent DECIMAL(5,2),
    days_to_close INT,
    
    -- Classification
    city VARCHAR(100),
    property_type VARCHAR(50),
    deal_tier VARCHAR(20),
    acquisition_price DECIMAL(12,2),
    sale_price DECIMAL(12,2),
    
    -- Timeline
    found_date TIMESTAMP,
    approved_date TIMESTAMP,
    contract_date TIMESTAMP,
    close_date TIMESTAMP,
    
    -- Status
    deal_status VARCHAR(50), -- completed, in_progress, rejected
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(property_id)
);

CREATE INDEX idx_profit_tracking_actual_profit ON profit_tracking(actual_profit DESC);
CREATE INDEX idx_profit_tracking_close_date ON profit_tracking(close_date);
CREATE INDEX idx_profit_tracking_city ON profit_tracking(city);
CREATE INDEX idx_profit_tracking_deal_status ON profit_tracking(deal_status);

-- ============================================
-- AUDIT & LOGS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Action Info
    action VARCHAR(100) NOT NULL,
    action_type VARCHAR(50), -- create, update, delete, approve, reject
    user_email VARCHAR(255),
    
    -- What Changed
    table_name VARCHAR(100),
    record_id UUID,
    changes TEXT, -- JSON of old vs new values
    
    -- Metadata
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    notes TEXT
);

CREATE INDEX idx_audit_logs_timestamp ON audit_logs(timestamp DESC);
CREATE INDEX idx_audit_logs_action_type ON audit_logs(action_type);

-- ============================================
-- SYSTEM SETTINGS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS system_settings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    setting_key VARCHAR(100) NOT NULL UNIQUE,
    setting_value TEXT,
    description TEXT,
    
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO system_settings (setting_key, setting_value, description) VALUES
    ('min_profit_threshold', '5000', 'Minimum profit per deal ($)'),
    ('max_profit_threshold', '100000', 'Maximum profit per deal ($)'),
    ('mao_arv_multiplier', '0.70', 'ARV multiplier for MAO calculation'),
    ('operation_fee', '10000', 'Operation/assignment fee ($)'),
    ('target_cities', '["Dallas","Fort Worth","Houston","Arlington","Mesquite"]', 'Target cities'),
    ('target_property_types', '["single-family","multi-family","land"]', 'Target property types'),
    ('min_days_to_auction', '14', 'Minimum days remaining to auction'),
    ('max_days_to_auction', '30', 'Maximum days remaining to auction'),
    ('arv_confidence_threshold', '70', 'Minimum ARV confidence score %'),
    ('last_scrape_time', 'null', 'Timestamp of last successful scrape'),
    ('scrape_interval_minutes', '120', 'Interval between scrapes (minutes)')
ON CONFLICT (setting_key) DO NOTHING;

-- ============================================
-- USERS TABLE (Team Access)
-- ============================================
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    email VARCHAR(255) NOT NULL UNIQUE,
    full_name VARCHAR(255),
    role VARCHAR(50), -- admin, analyst, approver, viewer
    
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- Create default admin user (UPDATE THIS)
INSERT INTO users (email, full_name, role) VALUES
    ('juancalude8001@gmail.com', 'Juan Claude Jordan', 'admin')
ON CONFLICT (email) DO NOTHING;

-- ============================================
-- MATERIALIZED VIEW: TOP DEALS
-- ============================================
CREATE MATERIALIZED VIEW IF NOT EXISTS top_deals AS
SELECT 
    p.id,
    p.address,
    p.city,
    p.property_type,
    p.opening_bid,
    a.arv_estimate,
    a.repair_estimate,
    a.mao,
    a.estimated_profit,
    a.deal_score,
    a.deal_tier,
    p.auction_date,
    p.time_remaining_days,
    CASE 
        WHEN ap.ready_for_outreach THEN 'Ready'
        WHEN ap.analysis_approved THEN 'Approved'
        ELSE 'Pending Review'
    END as approval_status
FROM properties p
LEFT JOIN analysis a ON p.id = a.property_id
LEFT JOIN approvals ap ON p.id = ap.property_id
WHERE a.deal_score >= 60
ORDER BY a.estimated_profit DESC, a.deal_score DESC
LIMIT 50;

-- ============================================
-- FUNCTION: Update Updated_At Timestamp
-- ============================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply to all tables with updated_at
CREATE TRIGGER update_properties_updated_at BEFORE UPDATE ON properties
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_approvals_updated_at BEFORE UPDATE ON approvals
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_offers_updated_at BEFORE UPDATE ON offers
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_deals_pipeline_updated_at BEFORE UPDATE ON deals_pipeline
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_profit_tracking_updated_at BEFORE UPDATE ON profit_tracking
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- FUNCTION: Log Audit Events
-- ============================================
CREATE OR REPLACE FUNCTION audit_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'DELETE' THEN
        INSERT INTO audit_logs (action_type, table_name, record_id, user_email, changes)
        VALUES ('delete', TG_TABLE_NAME, OLD.id, CURRENT_USER, to_jsonb(OLD));
        RETURN OLD;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_logs (action_type, table_name, record_id, user_email, changes)
        VALUES ('update', TG_TABLE_NAME, NEW.id, CURRENT_USER, 
                jsonb_build_object('old', to_jsonb(OLD), 'new', to_jsonb(NEW)));
        RETURN NEW;
    ELSIF TG_OP = 'INSERT' THEN
        INSERT INTO audit_logs (action_type, table_name, record_id, user_email, changes)
        VALUES ('insert', TG_TABLE_NAME, NEW.id, CURRENT_USER, to_jsonb(NEW));
        RETURN NEW;
    END IF;
    RETURN NULL;
END;
$$ language 'plpgsql';

-- Apply audit to approvals table (track human decisions)
CREATE TRIGGER audit_approvals
AFTER INSERT OR UPDATE OR DELETE ON approvals
FOR EACH ROW EXECUTE FUNCTION audit_changes();

-- Apply audit to offers table (track offer changes)
CREATE TRIGGER audit_offers
AFTER INSERT OR UPDATE OR DELETE ON offers
FOR EACH ROW EXECUTE FUNCTION audit_changes();

-- Apply audit to deals_pipeline (track deal status)
CREATE TRIGGER audit_deals_pipeline
AFTER INSERT OR UPDATE OR DELETE ON deals_pipeline
FOR EACH ROW EXECUTE FUNCTION audit_changes();

-- ============================================
-- INDEXES FOR PERFORMANCE
-- ============================================
CREATE INDEX idx_properties_city_type ON properties(city, property_type);
CREATE INDEX idx_properties_auction_date_city ON properties(auction_date, city);
CREATE INDEX idx_analysis_property_score ON analysis(property_id, deal_score DESC);
CREATE INDEX idx_offers_property_approved ON offers(property_id, human_approved);

-- ============================================
-- VIEW: DASHBOARD SUMMARY
-- ============================================
CREATE OR REPLACE VIEW dashboard_summary AS
SELECT 
    (SELECT COUNT(*) FROM properties WHERE created_at > NOW() - INTERVAL '24 hours') as properties_found_24h,
    (SELECT COUNT(*) FROM analysis WHERE deal_score >= 80) as gold_tier_deals,
    (SELECT COUNT(*) FROM analysis WHERE deal_score BETWEEN 60 AND 79) as silver_tier_deals,
    (SELECT COUNT(*) FROM approvals WHERE ready_for_outreach = TRUE) as deals_ready_for_outreach,
    (SELECT COUNT(*) FROM deals_pipeline WHERE status = 'under_contract') as active_contracts,
    (SELECT COALESCE(SUM(actual_profit), 0) FROM profit_tracking WHERE deal_status = 'completed') as total_profit_completed,
    (SELECT COALESCE(SUM(estimated_profit), 0) FROM analysis WHERE deal_tier = 'gold') as potential_profit_gold;
