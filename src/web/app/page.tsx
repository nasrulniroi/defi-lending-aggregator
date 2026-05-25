"use client";

import { useEffect, useState } from "react";

interface RateSummary {
  protocol: string;
  chain: string;
  supplyApy: number;
  borrowApy: number;
  tvl: number;
}

export default function Dashboard() {
  const [rates, setRates] = useState<RateSummary[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/rates")
      .then((r) => r.json())
      .then((d) => {
        setRates(d.data ?? []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  const topSupply = [...rates].sort((a, b) => b.supplyApy - a.supplyApy).slice(0, 5);
  const topBorrow = [...rates].sort((a, b) => a.borrowApy - b.borrowApy).slice(0, 5);

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-2xl font-bold text-gray-900">Dashboard</h2>
        <p className="mt-1 text-sm text-gray-500">Real-time lending rates across DeFi protocols</p>
      </div>

      <div className="grid grid-cols-1 gap-6 md:grid-cols-3">
        <div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
          <p className="text-sm font-medium text-gray-500">Protocols Tracked</p>
          <p className="mt-2 text-3xl font-bold text-indigo-600">{new Set(rates.map((r) => r.protocol)).size}</p>
        </div>
        <div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
          <p className="text-sm font-medium text-gray-500">Total TVL</p>
          <p className="mt-2 text-3xl font-bold text-indigo-600">
            ${rates.reduce((s, r) => s + r.tvl, 0).toLocaleString()}
          </p>
        </div>
        <div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
          <p className="text-sm font-medium text-gray-500">Avg Supply APY</p>
          <p className="mt-2 text-3xl font-bold text-indigo-600">
            {rates.length > 0 ? (rates.reduce((s, r) => s + r.supplyApy, 0) / rates.length).toFixed(2) : "0.00"}%
          </p>
        </div>
      </div>

      {loading ? (
        <div className="text-center text-gray-500">Loading rates...</div>
      ) : (
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
          <div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
            <h3 className="text-lg font-semibold text-gray-900">Top Supply Rates</h3>
            <div className="mt-4 space-y-3">
              {topSupply.map((r, i) => (
                <div key={i} className="flex items-center justify-between">
                  <div>
                    <span className="font-medium text-gray-900">{r.protocol}</span>
                    <span className="ml-2 text-sm text-gray-500">{r.chain}</span>
                  </div>
                  <span className="font-semibold text-green-600">{r.supplyApy.toFixed(2)}%</span>
                </div>
              ))}
            </div>
          </div>
          <div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
            <h3 className="text-lg font-semibold text-gray-900">Best Borrow Rates</h3>
            <div className="mt-4 space-y-3">
              {topBorrow.map((r, i) => (
                <div key={i} className="flex items-center justify-between">
                  <div>
                    <span className="font-medium text-gray-900">{r.protocol}</span>
                    <span className="ml-2 text-sm text-gray-500">{r.chain}</span>
                  </div>
                  <span className="font-semibold text-blue-600">{r.borrowApy.toFixed(2)}%</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
