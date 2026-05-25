import { NextResponse } from "next/server";

interface LendingRate {
  protocol: string;
  chain: string;
  asset: string;
  supplyApy: number;
  borrowApy: number;
  totalSupply: number;
  totalBorrow: number;
  utilizationRate: number;
  lastUpdated: string;
}

const MOCK_RATES: LendingRate[] = [
  { protocol: "Aave V3", chain: "Ethereum", asset: "USDC", supplyApy: 4.32, borrowApy: 6.18, totalSupply: 1250000000, totalBorrow: 680000000, utilizationRate: 0.544, lastUpdated: new Date().toISOString() },
  { protocol: "Aave V3", chain: "Ethereum", asset: "WETH", supplyApy: 2.87, borrowApy: 4.23, totalSupply: 890000000, totalBorrow: 420000000, utilizationRate: 0.472, lastUpdated: new Date().toISOString() },
  { protocol: "Aave V3", chain: "Arbitrum", asset: "USDC", supplyApy: 5.12, borrowApy: 7.45, totalSupply: 340000000, totalBorrow: 190000000, utilizationRate: 0.559, lastUpdated: new Date().toISOString() },
  { protocol: "Compound V3", chain: "Ethereum", asset: "USDC", supplyApy: 3.89, borrowApy: 5.67, totalSupply: 980000000, totalBorrow: 510000000, utilizationRate: 0.52, lastUpdated: new Date().toISOString() },
  { protocol: "Compound V3", chain: "Base", asset: "USDC", supplyApy: 6.21, borrowApy: 8.93, totalSupply: 120000000, totalBorrow: 72000000, utilizationRate: 0.6, lastUpdated: new Date().toISOString() },
  { protocol: "Morpho Blue", chain: "Ethereum", asset: "USDC", supplyApy: 5.45, borrowApy: 7.12, totalSupply: 450000000, totalBorrow: 230000000, utilizationRate: 0.511, lastUpdated: new Date().toISOString() },
  { protocol: "Morpho Blue", chain: "Ethereum", asset: "WETH", supplyApy: 3.14, borrowApy: 4.56, totalSupply: 320000000, totalBorrow: 150000000, utilizationRate: 0.469, lastUpdated: new Date().toISOString() },
  { protocol: "Benqi", chain: "Avalanche", asset: "USDC", supplyApy: 3.67, borrowApy: 5.89, totalSupply: 180000000, totalBorrow: 95000000, utilizationRate: 0.528, lastUpdated: new Date().toISOString() },
  { protocol: "Radiant", chain: "Arbitrum", asset: "USDT", supplyApy: 4.78, borrowApy: 6.95, totalSupply: 210000000, totalBorrow: 130000000, utilizationRate: 0.619, lastUpdated: new Date().toISOString() },
  { protocol: "Spark", chain: "Ethereum", asset: "DAI", supplyApy: 5.01, borrowApy: 6.78, totalSupply: 670000000, totalBorrow: 380000000, utilizationRate: 0.567, lastUpdated: new Date().toISOString() },
  { protocol: "Aave V3", chain: "Polygon", asset: "USDC", supplyApy: 4.89, borrowApy: 7.02, totalSupply: 280000000, totalBorrow: 160000000, utilizationRate: 0.571, lastUpdated: new Date().toISOString() },
  { protocol: "Compound V3", chain: "Arbitrum", asset: "WETH", supplyApy: 2.45, borrowApy: 3.89, totalSupply: 150000000, totalBorrow: 65000000, utilizationRate: 0.433, lastUpdated: new Date().toISOString() },
];

export async function GET() {
  return NextResponse.json({ data: MOCK_RATES, error: null, timestamp: new Date().toISOString() });
}
