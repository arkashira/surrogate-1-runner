import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { fetchRootCauseData } from '../services/api';
import { ResourceBreakdown, TimeRange } from '../types';

const RootCauseView: React.FC = () => {
  const { alertId } = useParams<{ alertId: string }>();
  const [rootCauseData, setRootCauseData] = useState<ResourceBreakdown[]>([]);
  const [timeRange, setTimeRange] = useState<TimeRange>('lastHour');
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const loadRootCauseData = async () => {
      setLoading(true);
      try {
        const data = await fetchRootCauseData(alertId, timeRange);
        setRootCauseData(data);
      } catch (error) {
        console.error('Failed to fetch root cause data:', error);
      } finally {
        setLoading(false);
      }
    };

    loadRootCauseData();
  }, [alertId, timeRange]);

  const handleTimeRangeChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setTimeRange(event.target.value as TimeRange);
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="root-cause-view">
      <h2>Root Cause Analysis</h2>
      <div className="time-range-filter">
        <label htmlFor="timeRange">Time Range:</label>
        <select id="timeRange" value={timeRange} onChange={handleTimeRangeChange}>
          <option value="lastHour">Last Hour</option>
          <option value="lastDay">Last Day</option>
        </select>
      </div>
      <div className="resource-breakdown">
        <h3>Top 5 Resources by Cost</h3>
        <table>
          <thead>
            <tr>
              <th>Resource Type</th>
              <th>Cost</th>
              <th>Percentage of Total</th>
              <th>Details</th>
            </tr>
          </thead>
          <tbody>
            {rootCauseData.map((resource, index) => (
              <tr key={index}>
                <td>{resource.resourceType}</td>
                <td>{resource.cost}</td>
                <td>{resource.percentage}%</td>
                <td>
                  <a href={`/costinel/resource/${resource.resourceId}`} target="_blank" rel="noopener noreferrer">
                    View Details
                  </a>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default RootCauseView;