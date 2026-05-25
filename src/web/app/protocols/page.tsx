"use client";

import { useEffect, useState } from "react";

interface Protocol {
  name: string;
  chains: string[];
  category: string;
  tvl: number;
  avgSupplyApy: number;
  avgBorrowApy: number;
  assetCount: number;
  status: string;
}

export default function ProtocolsPage() {
  const [protocols, setProtocols] = useState<Protocol[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/protocols")
      .then((r) => r.json())
      .then((d) => {
        setProtocols(d.data ?? []);
        setLoading(false);
      });
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900">Protocols</h2>
        <p className="mt-1 text-sm text-gray-500">Supported DeFi lending protocols</p>
      </div>

      {loading ? (
        <div className="text-center text-gray-500 py-12">Loading...</div>
      ) : (
        <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
          {protocols.map((p) => (
            <div key={p.name} className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-semibold text-indigo-600">{p.name}</h3>
                <span className={`rounded-full px-2 py-1 text-xs font-medium ${
                  p.status === "active" ? "bg-green-100 text-green-800" : "bg-yellow-100 text-yellow-800"
                }`}>{p.status}</span>
              </div>
              <p className="mt-1 text-sm text-gray-500">{p.category}</p>
              <div className="mt-4 space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-500">Chains</span>
                  <span className="text-gray-900">{p.chains.join(", ")}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">TVL</span>
                  <span className="text-gray-900">${p.tvl.toLocaleString()}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">Avg Supply</span>
                  <span className="font-medium text-green-600">{p.avgSupplyApy.toFixed(2)}%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">Avg Borrow</span>
                  <span className="font-medium text-blue-600">{p.avgBorrowApy.toFixed(2)}%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">Assets</span>
                  <span className="text-gray-900">{p.assetCount}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
