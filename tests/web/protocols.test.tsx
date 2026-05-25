import { render, screen, waitFor } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import ProtocolsPage from "@/app/protocols/page";

const mockProtocols = [
  { name: "Aave V3", chains: ["Ethereum", "Arbitrum"], category: "Lending", tvl: 12500000000, avgSupplyApy: 4.12, avgBorrowApy: 5.98, assetCount: 28, status: "active" },
];

describe("ProtocolsPage", () => {
  beforeEach(() => {
    vi.spyOn(global, "fetch").mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ data: mockProtocols, error: null, timestamp: new Date().toISOString() }),
    } as Response);
  });

  afterEach(() => vi.restoreAllMocks());

  it("renders protocol cards", async () => {
    render(<ProtocolsPage />);
    await waitFor(() => {
      expect(screen.getByText("Aave V3")).toBeTruthy();
    });
  });

  it("shows TVL", async () => {
    render(<ProtocolsPage />);
    await waitFor(() => {
      expect(screen.getByText("$12.50B")).toBeTruthy();
    });
  });

  it("shows chain badges", async () => {
    render(<ProtocolsPage />);
    await waitFor(() => {
      expect(screen.getByText("Ethereum")).toBeTruthy();
      expect(screen.getByText("Arbitrum")).toBeTruthy();
    });
  });
});
