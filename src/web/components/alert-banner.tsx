"use client";

import { useState } from "react";

interface AlertBannerProps {
  message: string;
  severity: "info" | "warning" | "critical";
  onDismiss?: () => void;
}

export function AlertBanner({ message, severity, onDismiss }: AlertBannerProps) {
  const [visible, setVisible] = useState(true);
  if (!visible) return null;

  const colors = {
    info: "bg-blue-50 border-blue-200 text-blue-800",
    warning: "bg-yellow-50 border-yellow-200 text-yellow-800",
    critical: "bg-red-50 border-red-200 text-red-800",
  };

  return (
    <div className={`flex items-center justify-between rounded-lg border p-3 ${colors[severity]}`}>
      <span className="text-sm font-medium">{message}</span>
      <button
        onClick={() => { setVisible(false); onDismiss?.(); }}
        className="ml-4 text-sm opacity-60 hover:opacity-100"
      >
        ✕
      </button>
    </div>
  );
}
