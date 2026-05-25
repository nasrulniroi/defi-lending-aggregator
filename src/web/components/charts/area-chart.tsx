"use client";

interface DataPoint {
  label: string;
  value: number;
}

interface AreaChartProps {
  data: DataPoint[];
  color?: string;
  height?: number;
  title?: string;
}

export function AreaChart({ data, color = "#818cf8", height = 200, title }: AreaChartProps) {
  if (data.length === 0) return null;

  const values = data.map((d) => d.value);
  const min = Math.min(...values) * 0.95;
  const max = Math.max(...values) * 1.05;
  const range = max - min || 1;

  const points = data.map((d, i) => {
    const x = (i / (data.length - 1)) * 100;
    const y = 100 - ((d.value - min) / range) * 100;
    return `${x},${y}`;
  });

  const pathD = `M 0,100 L ${points.join(" L ")} L 100,100 Z`;
  const lineD = `M ${points.join(" L ")}`;

  return (
    <div className="rounded-lg border border-gray-200 bg-white p-4 shadow-sm">
      {title && <h3 className="mb-3 text-sm font-semibold text-gray-700">{title}</h3>}
      <svg viewBox="0 0 100 100" preserveAspectRatio="none" className="w-full" style={{ height }}>
        <defs>
          <linearGradient id={`grad-${color.replace("#", "")}`} x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor={color} stopOpacity={0.3} />
            <stop offset="100%" stopColor={color} stopOpacity={0.05} />
          </linearGradient>
        </defs>
        <path d={pathD} fill={`url(#grad-${color.replace("#", "")})`} />
        <path d={lineD} fill="none" stroke={color} strokeWidth={0.5} vectorEffect="non-scaling-stroke" />
      </svg>
    </div>
  );
}
