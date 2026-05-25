"use client";

interface RateCardProps {
  protocol: string;
  chain: string;
  asset: string;
  supplyApy: number;
  borrowApy: number;
  utilizationRate: number;
}

export function RateCard({ protocol, chain, asset, supplyApy, borrowApy, utilizationRate }: RateCardProps) {
  return (
    <div className="rounded-lg border border-gray-200 bg-white p-4 shadow-sm transition-shadow hover:shadow-md">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-sm font-semibold text-gray-900">{protocol}</h3>
          <p className="text-xs text-gray-500">{chain} · {asset}</p>
        </div>
        <div className={`rounded-full px-2 py-0.5 text-xs font-medium ${
          utilizationRate > 0.8 ? "bg-red-100 text-red-700" : utilizationRate > 0.6 ? "bg-yellow-100 text-yellow-700" : "bg-green-100 text-green-700"
        }`}>
          {(utilizationRate * 100).toFixed(0)}% util
        </div>
      </div>
      <div className="mt-3 grid grid-cols-2 gap-2">
        <div>
          <p className="text-xs text-gray-500">Supply APY</p>
          <p className="text-lg font-bold text-green-600">{supplyApy.toFixed(2)}%</p>
        </div>
        <div>
          <p className="text-xs text-gray-500">Borrow APY</p>
          <p className="text-lg font-bold text-blue-600">{borrowApy.toFixed(2)}%</p>
        </div>
      </div>
    </div>
  );
}
