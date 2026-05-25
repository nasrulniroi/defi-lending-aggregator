"use client";

import { useEffect, useState } from "react";

interface Opportunity {
  asset: string;
  supplyProtocol: string;
  supplyChain: string;
  supplyApy: number;
  borrowProtocol: string;
  borrowChain: string;
  borrowApy: number;
  netApy: number;
  riskScore: number;
}

export default function OptimizerPage() {
  const [opportunities, setOpportunities] = useState<Opportunity[]>([]);
  const [loading, setLoading] = useState(true);
  const [minNetApy, setMinNetApy] = useState(0);

  useEffect(() => {
    fetch("/api/opportunities")
      .then((r) => r.json())
      .then((d) => {
        setOpportunities(d.data ?? []);
        setLoading(false);
      });
  }, []);

  const filtered = opportunities.filter((o) => o.netApy >= minNetApy);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Yield Optimizer</h2>
          <p className="mt-1 text-sm text-gray-500">Find the best leveraged yield opportunities</p>
        </div>
        <div className="flex items-center space-x-2">
          <label className="text-sm text-gray-500">Min Net APY:</label>
          <input
            type="number"
            value={minNetApy}
            onChange={(e) => setMinNetApy(Number(e.target.value))}
            className="w-20 rounded-md border border-gray-300 px-3 py-2 text-sm"
            step={0.5}
          />
          <span className="text-sm text-gray-500">%</span>
        </div>
      </div>

      {loading ? (
        <div className="text-center text-gray-500 py-12">Loading...</div>
      ) : (
        <div className="space-y-4">
          {filtered.map((o, i) => (
            <div key={i} className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">{o.asset}</h3>
                  <p className="text-sm text-gray-500">Leveraged yield strategy</p>
                </div>
                <div className="text-right">
                  <p className="text-2xl font-bold text-indigo-600">{o.netApy.toFixed(2)}%</p>
                  <p className="text-xs text-gray-500">Net APY</p>
                </div>
              </div>
              <div className="mt-4 grid grid-cols-2 gap-4">
                <div className="rounded bg-green-50 p-3">
                  <p className="text-xs font-medium text-green-800">Supply</p>
                  <p className="text-sm text-green-700">{o.supplyProtocol} ({o.supplyChain})</p>
                  <p className="text-lg font-semibold text-green-600">{o.supplyApy.toFixed(2)}%</p>
                </div>
                <div className="rounded bg-blue-50 p-3">
                  <p className="text-xs font-medium text-blue-800">Borrow</p>
                  <p className="text-sm text-blue-700">{o.borrowProtocol} ({o.borrowChain})</p>
                  <p className="text-lg font-semibold text-blue-600">{o.borrowApy.toFixed(2)}%</p>
                </div>
              </div>
              <div className="mt-3 flex items-center justify-between text-sm">
                <span className="text-gray-500">Risk Score: <span className={`font-medium ${
                  o.riskScore < 3 ? "text-green-600" : o.riskScore < 6 ? "text-yellow-600" : "text-red-600"
                }`}>{o.riskScore.toFixed(1)}/10</span></span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
