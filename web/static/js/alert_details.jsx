import React, { useEffect, useState } from 'react';
import axios from 'axios';

const AlertDetails = ({ alertId }) => {
  const [rootCauses, setRootCauses] = useState([]);
  const [metricsData, setMetricsData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAlertData = async () => {
      setLoading(true);
      try {
        const [rootCausesResponse, metricsResponse] = await Promise.all([
          axios.get(`/api/alert/${alertId}/root-causes`),
          axios.get(`/api/alert/${alertId}/metrics`),
        ]);
        
        setRootCauses(rootCausesResponse.data.slice(0, 3));
        setMetricsData(metricsResponse.data);
      } catch (error) {
        setError('Failed to fetch alert data');
        console.error('Error fetching alert data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchAlertData();
  }, [alertId]);

  const handleFeedback = (causeId, feedback) => {
    axios.post(`/api/alert/${alertId}/feedback`, { causeId, feedback })
      .then(() => console.log('Feedback sent successfully'))
      .catch(error => console.error('Error sending feedback:', error));
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <h2>Top Root Cause Hypotheses</h2>
      <ul>
        {rootCauses.map((cause, index) => (
          <li key={index}>
            {cause.description} ({cause.confidence.toFixed(2)})
            <button onClick={() => handleFeedback(cause.id, 'correct')}>Correct</button>
            <button onClick={() => handleFeedback(cause.id, 'incorrect')}>Incorrect</button>
          </li>
        ))}
      </ul>

      <h2>Related Metrics Graphs</h2>
      {metricsData && (
        <iframe
          title="Grafana Dashboard"
          src={`https://grafana.example.com/d-solo/${metricsData.dashboard}?orgId=1&var-datasource=${metricsData.datasource}`}
          width="100%"
          height="400px"
          frameBorder="0"
          aria-label="Grafana Dashboard for Alert Metrics"
        />
      )}
    </div>
  );
};

export default AlertDetails;