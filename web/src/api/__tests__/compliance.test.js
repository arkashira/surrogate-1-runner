/**
 * @jest-environment jsdom
 */
import { getComplianceStatus, listViolations, exportReport } from "../compliance";

// Mock the auth module to control token output.
jest.mock("../auth", () => ({
  getToken: jest.fn(() => "test-token-123"),
}));

// Enable fetch mocking.
global.fetch = jest.fn();

afterEach(() => {
  fetch.mockClear();
});

describe("compliance API client", () => {
  test("getComplianceStatus makes correct request and returns JSON", async () => {
    const mockData = { overall: "compliant", timestamp: "2026-05-14T00:00:00Z" };
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockData,
    });

    const result = await getComplianceStatus();

    expect(fetch).toHaveBeenCalledWith("/api/compliance/status", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer test-token-123",
      },
    });
    expect(result).toEqual(mockData);
  });

  test("listViolations builds query string and returns JSON", async () => {
    const mockData = { violations: [], page: 2, pageSize: 10 };
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockData,
    });

    const result = await listViolations({ page: 2, pageSize: 10 });

    expect(fetch).toHaveBeenCalledWith(
      "/api/compliance/violations?page=2&pageSize=10",
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer test-token-123",
        },
      }
    );
    expect(result).toEqual(mockData);
  });

  test("exportReport validates format and returns Blob", async () => {
    const mockBlob = new Blob(["dummy"], { type: "text/csv" });
    fetch.mockResolvedValueOnce({
      ok: true,
      blob: async () => mockBlob,
    });

    const result = await exportReport("csv");

    expect(fetch).toHaveBeenCalledWith("/api/compliance/export?format=csv", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer test-token-123",
      },
    });
    expect(result).toBe(mockBlob);
  });

  test("exportReport throws on unsupported format", async () => {
    await expect(exportReport("xml")).rejects.toThrow(
      'Invalid format: must be "csv" or "pdf"'
    );
    expect(fetch).not.toHaveBeenCalled();
  });
});