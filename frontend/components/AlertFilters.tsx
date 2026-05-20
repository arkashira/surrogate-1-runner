import React, { useState } from 'react';
import { Severity } from '../types/Alert';

interface AlertFiltersProps {
  onFilterChange: (severity: Severity[], source: string[]) => void;
}

const AlertFilters: React.FC<AlertFiltersProps> = ({ onFilterChange }) => {
  const [selectedSeverity, setSelectedSeverity] = useState<Severity[]>([]);
  const [selectedSource, setSelectedSource] = useState<string[]>([]);

  const handleSeverityChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const severity = event.target.value as Severity;
    if (selectedSeverity.includes(severity)) {
      setSelectedSeverity(selectedSeverity.filter((s) => s !== severity));
    } else {
      setSelectedSeverity([...selectedSeverity, severity]);
    }
  };

  const handleSourceChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const source = event.target.value;
    if (selectedSource.includes(source)) {
      setSelectedSource(selectedSource.filter((s) => s !== source));
    } else {
      setSelectedSource([...selectedSource, source]);
    }
  };

  const handleApplyFilters = () => {
    onFilterChange(selectedSeverity, selectedSource);
  };

  return (
    <div>
      <h2>Filter Alerts</h2>
      <div>
        <label>
          Severity:
          <input
            type="checkbox"
            value="critical"
            checked={selectedSeverity.includes('critical')}
            onChange={handleSeverityChange}
          />
          Critical
        </label>
        <label>
          <input
            type="checkbox"
            value="warning"
            checked={selectedSeverity.includes('warning')}
            onChange={handleSeverityChange}
          />
          Warning
        </label>
        <label>
          <input
            type="checkbox"
            value="info"
            checked={selectedSeverity.includes('info')}
            onChange={handleSeverityChange}
          />
          Info
        </label>
      </div>
      <div>
        <label>
          Source:
          <input
            type="checkbox"
            value="PagerDuty"
            checked={selectedSource.includes('PagerDuty')}
            onChange={handleSourceChange}
          />
          PagerDuty
        </label>
        <label>
          <input
            type="checkbox"
            value="CloudWatch"
            checked={selectedSource.includes('CloudWatch')}
            onChange={handleSourceChange}
          />
          CloudWatch
        </label>
      </div>
      <button onClick={handleApplyFilters}>Apply Filters</button>
    </div>
  );
};

export default AlertFilters;