-- Migration 002: Create lending rates and history tables
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

CREATE INDEX idx_rate_history_time ON rate_history(recorded_at DESC);
CREATE INDEX idx_rate_history_lookup ON rate_history(protocol_id, chain, asset, recorded_at DESC);
