"use client";

import { useEffect, useState } from "react";

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

export default function RatesPage() {
  const [rates, setRates] = useState<LendingRate[]>([]);
  const [loading, setLoading] = useState(true);
  const [chainFilter, setChainFilter] = useState("all");
  const [sortBy, setSortBy] = useState<"supply" | "borrow" | "utilization">("supply");

  useEffect(() => {
    fetch("/api/rates")
      .then((r) => r.json())
      .then((d) => {
        setRates(d.data ?? []);
        setLoading(false);
      });
  }, []);

  const chains = [...new Set(rates.map((r) => r.chain))].sort();

  const filtered = rates
    .filter((r) => chainFilter === "all" || r.chain === chainFilter)
    .sort((a, b) => {
      if (sortBy === "supply") return b.supplyApy - a.supplyApy;
      if (sortBy === "borrow") return a.borrowApy - b.borrowApy;
      return b.utilizationRate - a.utilizationRate;
    });

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Lending Rates</h2>
          <p className="mt-1 text-sm text-gray-500">Compare rates across all supported protocols</p>
        </div>
        <div className="flex space-x-3">
          <select
            value={chainFilter}
            onChange={(e) => setChainFilter(e.target.value)}
            className="rounded-md border border-gray-300 bg-white px-3 py-2 text-sm"
          >
            <option value="all">All Chains</option>
            {chains.map((c) => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as "supply" | "borrow" | "utilization")}
            className="rounded-md border border-gray-300 bg-white px-3 py-2 text-sm"
          >
            <option value="supply">Sort by Supply APY</option>
            <option value="borrow">Sort by Borrow APY</option>
            <option value="utilization">Sort by Utilization</option>
          </select>
        </div>
      </div>

      {loading ? (
        <div className="text-center text-gray-500 py-12">Loading...</div>
      ) : (
        <div className="overflow-hidden rounded-lg border border-gray-200 bg-white shadow-sm">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium uppercase text-gray-500">Protocol</th>
                <th className="px-6 py-3 text-left text-xs font-medium uppercase text-gray-500">Chain</th>
                <th className="px-6 py-3 text-left text-xs font-medium uppercase text-gray-500">Asset</th>
                <th className="px-6 py-3 text-right text-xs font-medium uppercase text-gray-500">Supply APY</th>
                <th className="px-6 py-3 text-right text-xs font-medium uppercase text-gray-500">Borrow APY</th>
                <th className="px-6 py-3 text-right text-xs font-medium uppercase text-gray-500">Utilization</th>
                <th className="px-6 py-3 text-right text-xs font-medium uppercase text-gray-500">TVL</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {filtered.map((r, i) => (
                <tr key={i} className="hover:bg-gray-50">
                  <td className="whitespace-nowrap px-6 py-4 text-sm font-medium text-gray-900">{r.protocol}</td>
                  <td className="whitespace-nowrap px-6 py-4 text-sm text-gray-500">{r.chain}</td>
                  <td className="whitespace-nowrap px-6 py-4 text-sm text-gray-500">{r.asset}</td>
                  <td className="whitespace-nowrap px-6 py-4 text-right text-sm font-semibold text-green-600">{r.supplyApy.toFixed(2)}%</td>
                  <td className="whitespace-nowrap px-6 py-4 text-right text-sm font-semibold text-blue-600">{r.borrowApy.toFixed(2)}%</td>
                  <td className="whitespace-nowrap px-6 py-4 text-right text-sm text-gray-500">{(r.utilizationRate * 100).toFixed(1)}%</td>
                  <td className="whitespace-nowrap px-6 py-4 text-right text-sm text-gray-500">${r.totalSupply.toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
