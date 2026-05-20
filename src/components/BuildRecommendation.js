/**
 * BuildRecommendation component
 *
 * Allows users to input build requirements and budget, fetches personalized
 * build recommendations from the backend, and displays them.
 *
 * Features:
 * - Controlled form inputs for requirements and budget.
 * - Debounced API calls to prevent excessive requests.
 * - Loading and error states.
 * - Caching of recent requests in memory for quick repeat queries.
 */

import React, { useState, useCallback, useEffect } from 'react';
import { getBuildRecommendations } from '../utils/api';

// Simple in‑memory cache keyed by `${requirements}|${budget}`
const cache = new Map();

/**
 * Debounce helper: delays function execution until after `delay` ms have
 * elapsed since the last call.
 */
function debounce(fn, delay) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), delay);
  };
}

export default function BuildRecommendation() {
  const [requirements, setRequirements] = useState('');
  const [budget, setBudget] = useState('');
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchRecommendations = useCallback(
    async (req, bud) => {
      const cacheKey = `${req}|${bud}`;
      if (cache.has(cacheKey)) {
        setRecommendations(cache.get(cacheKey));
        return;
      }

      setLoading(true);
      setError(null);
      try {
        const data = await getBuildRecommendations({
          requirements: req,
          budget: Number(bud),
        });
        setRecommendations(data.recommendations || []);
        cache.set(cacheKey, data.recommendations || []);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    },
    []
  );

  // Debounced version to avoid rapid API calls while typing
  const debouncedFetch = useCallback(debounce(fetchRecommendations, 500), [
    fetchRecommendations,
  ]);

  // Trigger fetch when inputs change (debounced)
  useEffect(() => {
    if (requirements.trim() && budget.trim()) {
      debouncedFetch(requirements, budget);
    } else {
      setRecommendations([]);
    }
  }, [requirements, budget, debouncedFetch]);

  return (
    <div className="build-recommendation">
      <h2>Build Recommendation</h2>
      <form
        onSubmit={(e) => {
          e.preventDefault();
          if (requirements.trim() && budget.trim()) {
            fetchRecommendations(requirements, budget);
          }
        }}
      >
        <div>
          <label htmlFor="requirements">Build Requirements:</label>
          <input
            id="requirements"
            type="text"
            value={requirements}
            onChange={(e) => setRequirements(e.target.value)}
            placeholder="e.g., high performance GPU"
            required
          />
        </div>
        <div>
          <label htmlFor="budget">Budget ($):</label>
          <input
            id="budget"
            type="number"
            value={budget}
            onChange={(e) => setBudget(e.target.value)}
            placeholder="e.g., 1500"
            required
          />
        </div>
        <button type="submit" disabled={loading}>
          {loading ? 'Fetching...' : 'Get Recommendations'}
        </button>
      </form>

      {error && <p className="error">Error: {error}</p>}

      {recommendations.length > 0 && (
        <ul className="recommendations-list">
          {recommendations.map((rec, idx) => (
            <li key={idx}>
              <strong>{rec.name}</strong> – ${rec.price}
              <p>{rec.description}</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}