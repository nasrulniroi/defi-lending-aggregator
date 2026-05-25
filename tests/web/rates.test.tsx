import { render, screen, waitFor } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import RatesPage from "@/app/rates/page";

const mockRates = [
  { protocol: "Aave V3", chain: "Ethereum", asset: "USDC", supplyApy: 4.32, borrowApy: 6.18, totalSupply: 1250000000, totalBorrow: 680000000, utilizationRate: 0.544, lastUpdated: new Date().toISOString() },
];

describe("RatesPage", () => {
  beforeEach(() => {
    vi.spyOn(global, "fetch").mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ data: mockRates, error: null, timestamp: new Date().toISOString() }),
    } as Response);
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("renders the rates page title", async () => {
    render(<RatesPage />);
    expect(screen.getByText("Lending Rates")).toBeTruthy();
  });

  it("displays rates after loading", async () => {
    render(<RatesPage />);
    await waitFor(() => {
      expect(screen.getByText("Aave V3")).toBeTruthy();
    });
  });

  it("shows supply and borrow APY", async () => {
    render(<RatesPage />);
    await waitFor(() => {
      expect(screen.getByText("4.32%")).toBeTruthy();
      expect(screen.getByText("6.18%")).toBeTruthy();
    });
  });
});
