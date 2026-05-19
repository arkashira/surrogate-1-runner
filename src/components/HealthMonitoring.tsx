import React, { useEffect, useState, useRef, useCallback } from 'react';
import './HealthMonitoring.css'; // Add your styles

type Service = {
  name: string;
  status: 'ok' | 'warning' | 'critical';
  lastChecked: string; // ISO string
};

type HealthResponse = {
  services: Service[];
};

export default function HealthMonitoring() {
  const [services, setServices] = useState<Service[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Keep a ref to the current AbortController so we can cancel stale requests
  const abortCtrlRef = useRef<AbortController | null>(null);

  const fetchHealth = useCallback(async () => {
    // Cancel any in‑flight request
    abortCtrlRef.current?.abort();
    const controller = new AbortController();
    abortCtrlRef.current = controller;

    try {
      const res = await fetch('/api/health', { signal: controller.signal });

      if (!res.ok) {
        throw new Error(`HTTP ${res.status} ${res.statusText}`);
      }

      const data: HealthResponse = await res.json();
      setServices(data.services ?? []);
      setError(null);
    } catch (err: any) {
      // Ignore abort errors – they’re expected on unmount or refresh
      if (err.name !== 'AbortError') {
        setError(err.message ?? 'Unknown error');
        setServices([]);
      }
    } finally {
      setLoading(false);
    }
  }, []);

  // Initial load + polling
  useEffect(() => {
    fetchHealth(); // initial fetch

    const interval = setInterval(fetchHealth, 30_000); // 30 s

    return () => {
      clearInterval(interval);
      abortCtrlRef.current?.abort(); // cancel any pending request
    };
  }, [fetchHealth]);

  // Derived data
  const criticalServices = services.filter((s) => s.status === 'critical');

  // Render
  if (loading) return <div className="hm-loading">Loading health data…</div>;

  if (error)
    return (
      <div className="hm-error">
        Failed to load health data: <strong>{error}</strong>
      </div>
    );

  return (
    <div className="health-monitoring">
      {criticalServices.length > 0 && (
        <div className="hm-alert hm-alert-critical">
          Critical issues detected in{' '}
          {criticalServices.length}{' '}
          {criticalServices.length === 1 ? 'service' : 'services'}!
        </div>
      )}

      <table className="hm-table">
        <thead>
          <tr>
            <th>Service</th>
            <th>Status</th>
            <th>Last Checked</th>
          </tr>
        </thead>
        <tbody>
          {services.map((svc) => (
            <tr key={svc.name} className={`hm-row hm-${svc.status}`}>
              <td>{svc.name}</td>
              <td>{svc.status}</td>
              <td>{new Date(svc.lastChecked).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}