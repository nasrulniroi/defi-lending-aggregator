INSERT INTO protocols (name, category, website, chains, status) VALUES
('Aave V3', 'lending', 'https://aave.com', '{"ethereum","arbitrum","polygon","base","avalanche"}', 'active'),
('Compound V3', 'lending', 'https://compound.finance', '{"ethereum","base","arbitrum","polygon"}', 'active'),
('Morpho Blue', 'lending', 'https://morpho.org', '{"ethereum"}', 'active'),
('Spark', 'lending', 'https://spark.fi', '{"ethereum"}', 'active'),
('Benqi', 'lending', 'https://benqi.fi', '{"avalanche"}', 'active'),
('Radiant', 'lending', 'https://radiant.capital', '{"arbitrum","ethereum","bsc"}', 'active'),
('Fluid', 'lending', 'https://fluid.instadapp.io', '{"ethereum","arbitrum"}', 'active'),
('Moonwell', 'lending', 'https://moonwell.fi', '{"base"}', 'active')
ON CONFLICT (name) DO NOTHING;
