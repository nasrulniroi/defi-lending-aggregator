export const CHAINS = [
  { id: "ethereum", name: "Ethereum", color: "#627EEA" },
  { id: "arbitrum", name: "Arbitrum", color: "#28A0F0" },
  { id: "polygon", name: "Polygon", color: "#8247E5" },
  { id: "base", name: "Base", color: "#0052FF" },
  { id: "avalanche", name: "Avalanche", color: "#E84142" },
] as const;

export const PROTOCOLS = [
  { id: "aave-v3", name: "Aave V3", category: "Lending" },
  { id: "compound-v3", name: "Compound V3", category: "Lending" },
  { id: "morpho-blue", name: "Morpho Blue", category: "Lending" },
  { id: "spark", name: "Spark", category: "Lending" },
  { id: "benqi", name: "Benqi", category: "Lending" },
  { id: "radiant", name: "Radiant", category: "Lending" },
  { id: "fluid", name: "Fluid", category: "Lending" },
  { id: "moonwell", name: "Moonwell", category: "Lending" },
] as const;

export const ASSETS = ["USDC", "USDT", "DAI", "WETH", "WBTC", "ETH", "AVAX", "MATIC"] as const;

export const REFRESH_INTERVAL = 60_000;
