"use client";

import { useEffect, useState } from "react";

interface Alert {
  id: string;
  type: string;
  protocol: string;
  chain: string;
  message: string;
  severity: "info" | "warning" | "critical";
  timestamp: string;
  read: boolean;
}

export default function AlertsPage() {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/rates")
      .then((r) => r.json())
      .then(() => {
        setAlerts([
          { id: "1", type: "rate_change", protocol: "Aave", chain: "Ethereum", message: "USDC supply rate dropped from 4.5% to 3.2%", severity: "warning", timestamp: new Date().toISOString(), read: false },
          { id: "2", type: "new_opportunity", protocol: "Compound", chain: "Base", message: "New high-yield opportunity: WETH at 8.7% supply APY", severity: "info", timestamp: new Date().toISOString(), read: false },
          { id: "3", type: "risk_alert", protocol: "Morpho", chain: "Ethereum", message: "Utilization rate above 95% for USDT market", severity: "critical", timestamp: new Date().toISOString(), read: true },
        ]);
        setLoading(false);
      });
  }, []);

  const markRead = (id: string) => {
    setAlerts((prev) => prev.map((a) => (a.id === id ? { ...a, read: true } : a)));
  };

  const severityColors = {
    info: "bg-blue-100 text-blue-800 border-blue-200",
    warning: "bg-yellow-100 text-yellow-800 border-yellow-200",
    critical: "bg-red-100 text-red-800 border-red-200",
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900">Alerts</h2>
        <p className="mt-1 text-sm text-gray-500">Rate changes, opportunities, and risk notifications</p>
      </div>

      {loading ? (
        <div className="text-center text-gray-500 py-12">Loading...</div>
      ) : (
        <div className="space-y-3">
          {alerts.map((a) => (
            <div
              key={a.id}
              className={`rounded-lg border p-4 shadow-sm ${a.read ? "bg-white border-gray-200" : "bg-indigo-50 border-indigo-200"}`}
            >
              <div className="flex items-start justify-between">
                <div className="flex items-start space-x-3">
                  <span className={`rounded-full px-2 py-1 text-xs font-medium ${severityColors[a.severity]}`}>
                    {a.severity}
                  </span>
                  <div>
                    <p className="font-medium text-gray-900">{a.protocol} · {a.chain}</p>
                    <p className="mt-1 text-sm text-gray-600">{a.message}</p>
                    <p className="mt-1 text-xs text-gray-400">{new Date(a.timestamp).toLocaleString()}</p>
                  </div>
                </div>
                {!a.read && (
                  <button onClick={() => markRead(a.id)} className="text-sm text-indigo-600 hover:text-indigo-800">
                    Mark read
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
