-- Migration 004: Create alerts table
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

CREATE INDEX idx_alerts_user ON alerts(user_id, is_read);
