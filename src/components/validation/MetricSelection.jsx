import React, { useState, useEffect } from 'react';
import axios from 'axios';

const PREDEFINED_METRICS = [
  { id: 'signups', name: 'Sign‑ups', unit: 'count' },
  { id: 'active_users', name: 'Active Users', unit: 'count' },
  { id: 'churn', name: 'Churn', unit: 'percentage' },
];

const UNIT_OPTIONS = ['count', 'percentage', 'time', 'currency'];

const MetricSelection = ({ projectId }) => {
  const [metrics, setMetrics] = useState([]);
  const [newMetric, setNewMetric] = useState({
    name: '',
    unit: 'count',
    target: '',
    timeframe: '',
  });

  // Load existing metrics
  useEffect(() => {
    axios
      .get(`/api/validation_project/${projectId}/metrics`)
      .then((res) => setMetrics(res.data))
      .catch((err) => console.error(err));
  }, [projectId]);

  const handleAddMetric = () => {
    const { name, unit, target, timeframe } = newMetric;
    if (!name || !unit || !target) return;

    const payload = { name, unit, target: Number(target), timeframe };
    axios
      .post(`/api/validation_project/${projectId}/metrics`, payload)
      .then((res) => {
        setMetrics([...metrics, res.data]);
        setNewMetric({ name: '', unit: 'count', target: '', timeframe: '' });
      })
      .catch((err) => console.error(err));
  };

  const handleTargetChange = (e, idx) => {
    const val = e.target.value;
    if (!/^\d*\.?\d*$/.test(val)) return; // numeric only
    const updated = [...metrics];
    updated[idx].target = val;
    setMetrics(updated);
  };

  const handleTimeframeChange = (e, idx) => {
    const updated = [...metrics];
    updated[idx].timeframe = e.target.value;
    setMetrics(updated);
  };

  return (
    <div className="metric-selection">
      <h3>Select Metrics</h3>
      <table className="metric-table">
        <thead>
          <tr>
            <th>Metric</th>
            <th>Unit</th>
            <th>Target</th>
            <th>Timeframe (optional)</th>
          </tr>
        </thead>
        <tbody>
          {metrics.map((m, idx) => (
            <tr key={idx}>
              <td>{m.name}</td>
              <td>{m.unit}</td>
              <td>
                <input
                  type="text"
                  value={m.target}
                  onChange={(e) => handleTargetChange(e, idx)}
                />
              </td>
              <td>
                <input
                  type="text"
                  value={m.timeframe}
                  onChange={(e) => handleTimeframeChange(e, idx)}
                />
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <h4>Add Custom Metric</h4>
      <div className="custom-metric-form">
        <input
          type="text"
          placeholder="Metric name"
          value={newMetric.name}
          onChange={(e) =>
            setNewMetric({ ...newMetric, name: e.target.value })
          }
        />
        <select
          value={newMetric.unit}
          onChange={(e) =>
            setNewMetric({ ...newMetric, unit: e.target.value })
          }
        >
          {UNIT_OPTIONS.map((u) => (
            <option key={u} value={u}>
              {u}
            </option>
          ))}
        </select>
        <input
          type="text"
          placeholder="Target"
          value={newMetric.target}
          onChange={(e) =>
            setNewMetric({ ...newMetric, target: e.target.value })
          }
        />
        <input
          type="text"
          placeholder="Timeframe (optional)"
          value={newMetric.timeframe}
          onChange={(e) =>
            setNewMetric({ ...newMetric, timeframe: e.target.value })
          }
        />
        <button onClick={handleAddMetric}>Add Metric</button>
      </div>
    </div>
  );
};

export default MetricSelection;