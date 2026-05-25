-- Migration 003: Create opportunities table
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

CREATE INDEX idx_opportunities_net_apy ON opportunities(net_apy DESC);
