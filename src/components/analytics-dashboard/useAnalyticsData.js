import { useEffect, useState, useRef } from "react";

/**
 * Hook that:
 *   • fetches historic data once (user‑engagement & onboarding flow)
 *   • subscribes to a live data source (WebSocket / SSE – here mocked with setInterval)
 *   • merges both streams into a single, time‑sorted array
 *   • returns { records, loading, error, unsubscribe }
 *
 * In production replace `mockSubscribe` with a real WebSocket/SSE client.
 */
export default function useAnalyticsData() {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const liveUnsubRef = useRef(() => {});

  // ---------- 1️⃣ Fetch historic data ----------
  useEffect(() => {
    async function fetchHistoric() {
      try {
        const [engRes, onbRes] = await Promise.all([
          fetch("/api/analytics/user-engagement"),
          fetch("/api/analytics/onboarding-flow-completion"),
        ]);

        if (!engRes.ok || !onbRes.ok) {
          throw new Error("Failed to load historic analytics");
        }

        const [engData, onbData] = await Promise.all([
          engRes.json(),
          onbRes.json(),
        ]);

        // Normalise historic rows to the same shape as live rows
        const historic = engData.map((e, i) => ({
          timestamp: e.date,
          activeUsers: e.userEngagement,
          completedOnboarding: onbData[i]?.onboardingFlowCompletion ?? 0,
          segment: "historic", // placeholder – you can enrich later
        }));

        setRecords((prev) => [...prev, ...historic].sort(byTimestampDesc));
      } catch (e) {
        console.error(e);
        setError(e);
      } finally {
        setLoading(false);
      }
    }

    fetchHistoric();
  }, []);

  // ---------- 2️⃣ Subscribe to live data ----------
  useEffect(() => {
    // ---- Mock implementation – replace with real WS/SSE ----
    function mockSubscribe(callback) {
      const interval = setInterval(() => {
        const now = new Date().toISOString();
        const data = {
          timestamp: now,
          activeUsers: Math.floor(Math.random() * 500) + 50,
          completedOnboarding: Math.floor(Math.random() * 300) + 20,
          segment: ["US", "EU", "APAC"][Math.floor(Math.random() * 3)],
        };
        callback(data);
      }, 1000);
      return () => clearInterval(interval);
    }

    const unsubscribe = mockSubscribe((liveRow) => {
      setRecords((prev) => {
        const merged = [...prev, liveRow].sort(byTimestampDesc);
        // Keep only the most recent N rows to avoid unbounded memory growth
        return merged.slice(0, 500);
      });
    });

    liveUnsubRef.current = unsubscribe;
    return unsubscribe;
  }, []);

  // ---------- Helper ----------
  const byTimestampDesc = (a, b) =>
    new Date(b.timestamp) - new Date(a.timestamp);

  return {
    records,
    loading,
    error,
    unsubscribeLive: liveUnsubRef.current,
  };
}