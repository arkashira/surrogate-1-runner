const API_BASE = '/api';

async function handleResponse(response) {
  if (!response.ok) {
    throw new Error(`API Error: ${response.status} ${response.statusText}`);
  }
  return response.json();
}

export async function fetchAuditItems() {
  const response = await fetch(`${API_BASE}/audit-items`);
  return handleResponse(response);
}

export async function fetchCommitDiff(commitSha) {
  const response = await fetch(`${API_BASE}/commits/${commitSha}/diff`);
  return handleResponse(response);
}