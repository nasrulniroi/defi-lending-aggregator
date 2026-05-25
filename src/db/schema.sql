CREATE TABLE IF NOT EXISTS protocols (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    category VARCHAR(50) NOT NULL DEFAULT 'lending',
    website VARCHAR(255),
    docs_url VARCHAR(255),
    github_url VARCHAR(255),
    chains TEXT[] NOT NULL DEFAULT '{}',
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS lending_rates (
    id SERIAL PRIMARY KEY,
    protocol_id INTEGER NOT NULL REFERENCES protocols(id),
    chain VARCHAR(50) NOT NULL,
    asset VARCHAR(20) NOT NULL,
    supply_apy DECIMAL(10, 4) NOT NULL,
    borrow_apy DECIMAL(10, 4) NOT NULL,
    total_supply DECIMAL(30, 2) NOT NULL DEFAULT 0,
    total_borrow DECIMAL(30, 2) NOT NULL DEFAULT 0,
    utilization_rate DECIMAL(6, 4) NOT NULL DEFAULT 0,
    supply_rate_per_block DECIMAL(20, 12),
    borrow_rate_per_block DECIMAL(20, 12),
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(protocol_id, chain, asset)
);

CREATE TABLE IF NOT EXISTS rate_history (
    id SERIAL PRIMARY KEY,
    protocol_id INTEGER NOT NULL REFERENCES protocols(id),
    chain VARCHAR(50) NOT NULL,
    asset VARCHAR(20) NOT NULL,
    supply_apy DECIMAL(10, 4) NOT NULL,
    borrow_apy DECIMAL(10, 4) NOT NULL,
    total_supply DECIMAL(30, 2) NOT NULL,
    total_borrow DECIMAL(30, 2) NOT NULL,
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS opportunities (
    id SERIAL PRIMARY KEY,
    asset VARCHAR(20) NOT NULL,
    supply_protocol_id INTEGER NOT NULL REFERENCES protocols(id),
    supply_chain VARCHAR(50) NOT NULL,
    supply_apy DECIMAL(10, 4) NOT NULL,
    borrow_protocol_id INTEGER NOT NULL REFERENCES protocols(id),
    borrow_chain VARCHAR(50) NOT NULL,
    borrow_apy DECIMAL(10, 4) NOT NULL,
    net_apy DECIMAL(10, 4) NOT NULL,
    risk_score DECIMAL(4, 2) NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS alerts (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(100),
    alert_type VARCHAR(50) NOT NULL,
    protocol_id INTEGER REFERENCES protocols(id),
    chain VARCHAR(50),
    asset VARCHAR(20),
    threshold_value DECIMAL(10, 4),
    message TEXT NOT NULL,
    severity VARCHAR(20) NOT NULL DEFAULT 'info',
    is_read BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_lending_rates_protocol ON lending_rates(protocol_id);
CREATE INDEX idx_lending_rates_chain_asset ON lending_rates(chain, asset);
CREATE INDEX idx_rate_history_time ON rate_history(recorded_at DESC);
CREATE INDEX idx_rate_history_lookup ON rate_history(protocol_id, chain, asset, recorded_at DESC);
CREATE INDEX idx_alerts_user ON alerts(user_id, is_read);
CREATE INDEX idx_opportunities_net_apy ON opportunities(net_apy DESC);
