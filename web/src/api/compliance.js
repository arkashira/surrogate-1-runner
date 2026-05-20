import { getToken } from "./auth";

/**
 * Base URL for backend API calls.
 * Adjust via environment variable if needed.
 */
const API_ROOT = process.env.REACT_APP_API_ROOT || "/api";

/**
 * Construct request headers, injecting the bearer token from the
 * existing authentication system.
 */
function buildHeaders() {
  const token = getToken();
  return {
    "Content-Type": "application/json",
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };
}

/**
 * Fetch the overall compliance status.
 *
 * @returns {Promise<Object>} JSON payload describing overall status.
 * @throws {Error} on non‑2xx HTTP responses.
 */
export async function getComplianceStatus() {
  const response = await fetch(`${API_ROOT}/compliance/status`, {
    method: "GET",
    headers: buildHeaders(),
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(
      `Failed to fetch compliance status: ${response.status} ${text}`
    );
  }

  return response.json();
}

/**
 * Retrieve a paginated list of current policy violations.
 *
 * @param {Object} [options] Pagination options.
 * @param {number} [options.page=1] Page number (1‑based).
 * @param {number} [options.pageSize=20] Items per page.
 * @returns {Promise<Object>} JSON payload containing violations.
 * @throws {Error} on non‑2xx HTTP responses.
 */
export async function listViolations({ page = 1, pageSize = 20 } = {}) {
  const params = new URLSearchParams({ page: String(page), pageSize: String(pageSize) });
  const response = await fetch(`${API_ROOT}/compliance/violations?${params}`, {
    method: "GET",
    headers: buildHeaders(),
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(
      `Failed to fetch violations: ${response.status} ${text}`
    );
  }

  return response.json();
}

/**
 * Export the compliance report in the requested format.
 *
 * @param {string} format Either "csv" or "pdf".
 * @returns {Promise<Blob>} Binary blob suitable for download.
 * @throws {Error} on invalid format or non‑2xx HTTP responses.
 */
export async function exportReport(format = "csv") {
  if (!["csv", "pdf"].includes(format)) {
    throw new Error('Invalid format: must be "csv" or "pdf"');
  }

  const response = await fetch(`${API_ROOT}/compliance/export?format=${format}`, {
    method: "GET",
    headers: buildHeaders(),
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(
      `Failed to export report: ${response.status} ${text}`
    );
  }

  // The backend returns a file; expose it as a Blob for the UI to download.
  return response.blob();
}