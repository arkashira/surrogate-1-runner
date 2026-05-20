import React from "react";
import { render, screen, waitFor } from "@testing-library/react";
import AlertsPanel from "./AlertsPanel";

// Mock the global fetch API
global.fetch = jest.fn();

const mockAlerts = [
  {
    id: "a1",
    message: "Unexpected spike in EC2 usage",
    timestamp: "2026-05-16T10:00:00Z",
    rootCause: "New auto‑scaling group launched",
  },
  {
    id: "a2",
    message: "S3 storage cost increased 40%",
    timestamp: "2026-05-16T09:55:00Z",
  },
];

beforeEach(() => {
  fetch.mockReset();
});

test("renders alerts fetched from the API", async () => {
  fetch.mockResolvedValueOnce({
    ok: true,
    json: async () => mockAlerts,
  });

  render(<AlertsPanel pollIntervalMs={1000000} />); // long interval to avoid extra polls

  // Verify loading state (no alerts yet)
  expect(screen.getByText(/No active anomalies/i)).toBeInTheDocument();

  // Wait for the fetch to resolve and UI to update
  await waitFor(() => {
    expect(screen.getByText(/Unexpected spike in EC2 usage/i)).toBeInTheDocument();
    expect(screen.getByText(/S3 storage cost increased 40%/i)).toBeInTheDocument();
  });

  // Verify timestamps are rendered (locale‑dependent, so check substring)
  expect(screen.getAllByText(/2026/).length).toBe(2);

  // Verify root‑cause suggestion appears only for the first alert
  expect(
    screen.getByText(/Suggested root cause: New auto‑scaling group launched/i)
  ).toBeInTheDocument();
  expect(
    screen.queryByText(/Suggested root cause:/i, { selector: "span" })
  ).toHaveTextContent(/New auto‑scaling group launched/);
});

test("displays an error message when the API fails", async () => {
  fetch.mockResolvedValueOnce({
    ok: false,
    status: 500,
  });

  render(<AlertsPanel pollIntervalMs={1000000} />);

  await waitFor(() => {
    expect(
      screen.getByRole("alert", { name: /Unable to load alerts/i })
    ).toBeInTheDocument();
  });
});