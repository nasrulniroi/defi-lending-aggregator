const BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "";

interface ApiResponse<T> {
  data: T;
  error: string | null;
  timestamp: string;
}

async function request<T>(endpoint: string): Promise<ApiResponse<T>> {
  const res = await fetch(`${BASE_URL}${endpoint}`, {
    headers: { "Content-Type": "application/json" },
    next: { revalidate: 60 },
  });

  if (!res.ok) {
    throw new Error(`API error: ${res.status} ${res.statusText}`);
  }

  return res.json();
}

export const api = {
  getRates: () => request("/api/rates"),
  getProtocols: () => request("/api/protocols"),
  getOpportunities: () => request("/api/opportunities"),
};
