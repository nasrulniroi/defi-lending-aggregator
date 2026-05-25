"use client";

interface OpportunityCardProps {
  asset: string;
  supplyProtocol: string;
  supplyApy: number;
  borrowProtocol: string;
  borrowApy: number;
  netApy: number;
  riskScore: number;
}

export function OpportunityCard({ asset, supplyProtocol, supplyApy, borrowProtocol, borrowApy, netApy, riskScore }: OpportunityCardProps) {
  return (
    <div className="rounded-lg border border-gray-200 bg-white p-5 shadow-sm">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-bold text-gray-900">{asset}</h3>
        <span className="text-2xl font-bold text-indigo-600">{netApy.toFixed(2)}%</span>
      </div>
      <div className="mt-3 grid grid-cols-2 gap-3">
        <div className="rounded bg-green-50 p-2">
          <p className="text-xs text-green-700">Supply: {supplyProtocol}</p>
          <p className="font-semibold text-green-600">{supplyApy.toFixed(2)}%</p>
        </div>
        <div className="rounded bg-blue-50 p-2">
          <p className="text-xs text-blue-700">Borrow: {borrowProtocol}</p>
          <p className="font-semibold text-blue-600">{borrowApy.toFixed(2)}%</p>
        </div>
      </div>
      <div className="mt-2 flex items-center justify-between text-xs">
        <span className="text-gray-500">Net APY: {netApy.toFixed(2)}%</span>
        <span className={`font-medium ${riskScore < 3 ? "text-green-600" : riskScore < 6 ? "text-yellow-600" : "text-red-600"}`}>
          Risk: {riskScore.toFixed(1)}/10
        </span>
      </div>
    </div>
  );
}
