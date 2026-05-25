"use client";

interface ProtocolCardProps {
  name: string;
  chains: string[];
  tvl: number;
  avgSupplyApy: number;
  assetCount: number;
}

export function ProtocolCard({ name, chains, tvl, avgSupplyApy, assetCount }: ProtocolCardProps) {
  const formatTvl = (v: number) => {
    if (v >= 1e9) return `$${(v / 1e9).toFixed(2)}B`;
    if (v >= 1e6) return `$${(v / 1e6).toFixed(1)}M`;
    return `$${v.toLocaleString()}`;
  };

  return (
    <div className="rounded-lg border border-gray-200 bg-white p-5 shadow-sm">
      <h3 className="text-lg font-semibold text-indigo-600">{name}</h3>
      <div className="mt-2 flex flex-wrap gap-1">
        {chains.map((c) => (
          <span key={c} className="rounded-full bg-indigo-50 px-2 py-0.5 text-xs font-medium text-indigo-700">{c}</span>
        ))}
      </div>
      <div className="mt-3 grid grid-cols-3 gap-2 text-sm">
        <div>
          <p className="text-gray-500">TVL</p>
          <p className="font-semibold text-gray-900">{formatTvl(tvl)}</p>
        </div>
        <div>
          <p className="text-gray-500">Avg Supply</p>
          <p className="font-semibold text-green-600">{avgSupplyApy.toFixed(2)}%</p>
        </div>
        <div>
          <p className="text-gray-500">Assets</p>
          <p className="font-semibold text-gray-900">{assetCount}</p>
        </div>
      </div>
    </div>
  );
}
