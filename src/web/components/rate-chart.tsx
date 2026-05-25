"use client";

import { useEffect, useRef } from "react";

interface DataPoint {
  timestamp: string;
  supplyApy: number;
  borrowApy: number;
}

interface RateChartProps {
  data: DataPoint[];
  protocol: string;
  asset: string;
}

export function RateChart({ data, protocol, asset }: RateChartProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas || data.length === 0) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const width = canvas.width;
    const height = canvas.height;
    const padding = { top: 20, right: 20, bottom: 30, left: 50 };

    ctx.clearRect(0, 0, width, height);

    const allValues = data.flatMap((d) => [d.supplyApy, d.borrowApy]);
    const minVal = Math.min(...allValues) * 0.9;
    const maxVal = Math.max(...allValues) * 1.1;

    const xScale = (i: number) => padding.left + (i / (data.length - 1)) * (width - padding.left - padding.right);
    const yScale = (v: number) => height - padding.bottom - ((v - minVal) / (maxVal - minVal)) * (height - padding.top - padding.bottom);

    // Grid lines
    ctx.strokeStyle = "#f3f4f6";
    ctx.lineWidth = 1;
    for (let i = 0; i <= 4; i++) {
      const y = padding.top + (i / 4) * (height - padding.top - padding.bottom);
      ctx.beginPath();
      ctx.moveTo(padding.left, y);
      ctx.lineTo(width - padding.right, y);
      ctx.stroke();
    }

    // Supply line (green)
    ctx.strokeStyle = "#16a34a";
    ctx.lineWidth = 2;
    ctx.beginPath();
    data.forEach((d, i) => {
      const x = xScale(i);
      const y = yScale(d.supplyApy);
      i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
    });
    ctx.stroke();

    // Borrow line (blue)
    ctx.strokeStyle = "#2563eb";
    ctx.lineWidth = 2;
    ctx.beginPath();
    data.forEach((d, i) => {
      const x = xScale(i);
      const y = yScale(d.borrowApy);
      i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
    });
    ctx.stroke();

    // Legend
    ctx.fillStyle = "#16a34a";
    ctx.fillRect(width - 150, 10, 12, 12);
    ctx.fillStyle = "#374151";
    ctx.font = "11px sans-serif";
    ctx.fillText("Supply APY", width - 133, 20);

    ctx.fillStyle = "#2563eb";
    ctx.fillRect(width - 150, 28, 12, 12);
    ctx.fillStyle = "#374151";
    ctx.fillText("Borrow APY", width - 133, 38);
  }, [data]);

  return (
    <div className="rounded-lg border border-gray-200 bg-white p-4 shadow-sm">
      <h3 className="mb-2 text-sm font-semibold text-gray-700">{protocol} · {asset} Rate History</h3>
      <canvas ref={canvasRef} width={600} height={200} className="w-full" />
    </div>
  );
}
