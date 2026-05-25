import { NextResponse } from "next/server";

const PROTOCOLS = [
  { name: "Aave V3", chains: ["Ethereum", "Arbitrum", "Polygon", "Base", "Avalanche"], category: "Lending", tvl: 12500000000, avgSupplyApy: 4.12, avgBorrowApy: 5.98, assetCount: 28, status: "active" },
  { name: "Compound V3", chains: ["Ethereum", "Base", "Arbitrum", "Polygon"], category: "Lending", tvl: 8200000000, avgSupplyApy: 3.95, avgBorrowApy: 5.72, assetCount: 15, status: "active" },
  { name: "Morpho Blue", chains: ["Ethereum"], category: "Lending", tvl: 3400000000, avgSupplyApy: 4.67, avgBorrowApy: 6.34, assetCount: 12, status: "active" },
  { name: "Spark", chains: ["Ethereum"], category: "Lending", tvl: 4100000000, avgSupplyApy: 5.01, avgBorrowApy: 6.78, assetCount: 8, status: "active" },
  { name: "Benqi", chains: ["Avalanche"], category: "Lending", tvl: 980000000, avgSupplyApy: 3.67, avgBorrowApy: 5.89, assetCount: 10, status: "active" },
  { name: "Radiant", chains: ["Arbitrum", "Ethereum", "BSC"], category: "Lending", tvl: 560000000, avgSupplyApy: 4.78, avgBorrowApy: 6.95, assetCount: 14, status: "active" },
  { name: "Fluid", chains: ["Ethereum", "Arbitrum"], category: "Lending", tvl: 1200000000, avgSupplyApy: 5.23, avgBorrowApy: 7.12, assetCount: 6, status: "active" },
  { name: "Moonwell", chains: ["Base"], category: "Lending", tvl: 340000000, avgSupplyApy: 5.45, avgBorrowApy: 7.89, assetCount: 8, status: "active" },
];

export async function GET() {
  return NextResponse.json({ data: PROTOCOLS, error: null, timestamp: new Date().toISOString() });
}
