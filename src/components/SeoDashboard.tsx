import React, { useEffect, useState } from 'react';
import './SeoDashboard.css';

interface Metric {
  id: string;
  title: string;
  value: string | number;
  icon: string;
  trend?: 'up' | 'down' | 'neutral'; // Optional: for future trend analysis
}

const SeoDashboard: React.FC = () => {
  const [metrics, setMetrics] = useState<Metric[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  // Simulate real-time updates with polling every 30 seconds
  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        // TODO: Replace with actual API call to your backend ingestion service
        // Example: const response = await fetch('http://localhost:3000/api/seo-metrics');
        
        // MOCK DATA (Remove this block when backend is connected)
        const mockData: Metric[] = [
          { id: '1', title: 'Organic Traffic', value: 12456, icon: '📈', trend: 'up' },
          { id: '2', title: 'Keyword Rankings', value: 342, icon: '🔑', trend: 'up' },
          { id: '3', title: 'Backlinks', value: 876, icon: '🔗', trend: 'neutral' },
          { id: '4', title: 'Crawl Errors', value: 12, icon: '⚠️', trend: 'down' },
        ];
        
        setMetrics(mockData);
        setLoading(false);
      } catch (error) {
        console.error("Failed to fetch SEO metrics:", error);
        setLoading(false);
      }
    };

    fetchMetrics();
    const interval = setInterval(fetchMetrics, 30000);
    return () => clearInterval(interval);
  }, []);

  if (loading) return <div className="seo-dashboard-loading">Loading SEO Data...</div>;

  return (
    <div className="seo-dashboard">
      <h2>SEO Performance Dashboard</h2>
      <div className="metrics-grid">
        {metrics.map((m) => (
          <div key={m.id} className="metric-card">
            <div className="metric-icon">{m.icon}</div>
            <div className="metric-info">
              <span className="metric-title">{m.title}</span>
              <span className="metric-value">{m.value}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SeoDashboard;