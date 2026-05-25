import { NextResponse } from "next/server";

const OPPORTUNITIES = [
  { asset: "USDC", supplyProtocol: "Compound V3", supplyChain: "Base", supplyApy: 6.21, borrowProtocol: "Aave V3", borrowChain: "Ethereum", borrowApy: 4.32, netApy: 1.89, riskScore: 2.3 },
  { asset: "WETH", supplyProtocol: "Morpho Blue", supplyChain: "Ethereum", supplyApy: 3.14, borrowProtocol: "Compound V3", borrowChain: "Arbitrum", borrowApy: 2.45, netApy: 0.69, riskScore: 1.8 },
  { asset: "USDC", supplyProtocol: "Radiant", supplyChain: "Arbitrum", supplyApy: 4.78, borrowProtocol: "Aave V3", borrowChain: "Ethereum", borrowApy: 4.32, netApy: 0.46, riskScore: 3.1 },
  { asset: "USDC", supplyProtocol: "Spark", supplyChain: "Ethereum", supplyApy: 5.01, borrowProtocol: "Compound V3", borrowChain: "Ethereum", borrowApy: 3.89, netApy: 1.12, riskScore: 2.0 },
  { asset: "DAI", supplyProtocol: "Spark", supplyChain: "Ethereum", supplyApy: 5.01, borrowProtocol: "Aave V3", borrowChain: "Ethereum", borrowApy: 4.32, netApy: 0.69, riskScore: 2.1 },
  { asset: "USDC", supplyProtocol: "Moonwell", supplyChain: "Base", supplyApy: 5.45, borrowProtocol: "Aave V3", borrowChain: "Ethereum", borrowApy: 4.32, netApy: 1.13, riskScore: 3.5 },
  { asset: "USDT", supplyProtocol: "Radiant", supplyChain: "Arbitrum", supplyApy: 4.78, borrowProtocol: "Compound V3", borrowChain: "Ethereum", borrowApy: 3.89, netApy: 0.89, riskScore: 2.8 },
];

export async function GET() {
  return NextResponse.json({ data: OPPORTUNITIES, error: null, timestamp: new Date().toISOString() });
}
