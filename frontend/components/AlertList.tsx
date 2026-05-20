import React, { useState, useEffect } from 'react';
import AlertFilters from './AlertFilters';
import { Alert } from '../types/Alert';

interface AlertListProps {
  alerts: Alert[];
}

const AlertList: React.FC<AlertListProps> = ({ alerts }) => {
  const [filteredAlerts, setFilteredAlerts] = useState(alerts);
  const [severityFilter, setSeverityFilter] = useState<Alert['severity'][]>([]);
  const [sourceFilter, setSourceFilter] = useState<string[]>([]);

  const handleFilterChange = (severity: Alert['severity'][], source: string[]) => {
    setSeverityFilter(severity);
    setSourceFilter(source);
  };

  useEffect(() => {
    const filtered = alerts.filter((alert) => {
      const severityMatch = severityFilter.length === 0 || severityFilter.includes(alert.severity);
      const sourceMatch = sourceFilter.length === 0 || sourceFilter.includes(alert.source);
      return severityMatch && sourceMatch;
    });
    setFilteredAlerts(filtered);
  }, [alerts, severityFilter, sourceFilter]);

  return (
    <div>
      <AlertFilters onFilterChange={handleFilterChange} />
      <ul>
        {filteredAlerts.map((alert) => (
          <li key={alert.title}>
            <span style={{ color: getSeverityColor(alert.severity) }}>{alert.title}</span>
            <span> ({alert.source})</span>
            <span> {alert.timestamp}</span>
            <span> {alert.affectedService}</span>
          </li>
        ))}
      </ul>
    </div>
  );
};

const getSeverityColor = (severity: Alert['severity']) => {
  switch (severity) {
    case 'critical':
      return 'red';
    case 'warning':
      return 'orange';
    case 'info':
      return 'green';
    default:
      return 'black';
  }
};

export default AlertList;