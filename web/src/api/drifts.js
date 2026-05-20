import axios from "axios";

/**
 * Retrieve the latest drift events from the backend.
 *
 * The backend may return either:
 *   • a plain array:          [{…}, …]
 *   • an object with a key:  { drifts: [{…}, …] }
 *
 * The function normalises both shapes to a plain array.
 *
 * @returns {Promise<Array<Object>>}  Resolves with an array of drift objects.
 *   Each object should contain:
 *     - service   (string)
 *     - deployment(string)
 *     - timestamp (ISO‑8601 string)
 *     - diff      (string, raw diff)
 */
export async function getDrifts() {
  // The global Axios instance already has auth interceptors, baseURL, etc.
  const response = await axios.get("/api/drifts", { timeout: 10_000 });

  // Normalise the payload.
  if (Array.isArray(response.data)) {
    return response.data;
  }
  if (response.data && Array.isArray(response.data.drifts)) {
    return response.data.drifts;
  }

  // Unexpected shape – return an empty list so the UI stays stable.
  console.warn("Unexpected drift payload:", response.data);
  return [];
}