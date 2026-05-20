/**
 * API utility for fetching build recommendations.
 *
 * The backend expects a POST request to `/api/recommendations` with a JSON
 * payload containing `requirements` (string) and `budget` (number).
 *
 * The function returns a promise that resolves to the parsed JSON response.
 * It throws an error if the HTTP status is not in the 200–299 range.
 */

export async function getBuildRecommendations({ requirements, budget }) {
  const response = await fetch('/api/recommendations', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ requirements, budget }),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(
      `Failed to fetch recommendations: ${response.status} ${errorText}`
    );
  }

  return response.json();
}